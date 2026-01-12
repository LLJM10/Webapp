from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings
from django.db.models import Sum, Avg, Count, Q
from datetime import datetime, timedelta
from decimal import Decimal
import math

from .models import Todo, Pitch, Event, SavedPitch, Investment
from .serializers import TodoSerializer, PitchSerializer, EventSerializer, SavedPitchSerializer, InvestmentSerializer

#Test API Call
@api_view(["GET"])
def hello(request):
    return Response({"message": "Hallo von Django!"})


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class IsOwnerOrReadOnly(BasePermission):
    """Nur Owner darf bearbeiten/löschen"""
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.owner == request.user


class PitchViewSet(viewsets.ModelViewSet):
    """Modell für Pitches"""
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        
        if self.request.query_params.get('mine') in ['1', 'true', 'True']:
            if self.request.user.is_authenticated:
                return qs.filter(owner=self.request.user)
            else:
                return qs.none()
        
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return qs
        else:
            return qs.filter(is_public=True)
        
        return qs


class EventViewSet(viewsets.ModelViewSet):
    """Modell für Events"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        
        if self.request.query_params.get('mine') in ['1', 'true', 'True']:
            if self.request.user.is_authenticated:
                return qs.filter(owner=self.request.user)
            else:
                return qs.none()
        
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return qs
        else:
            return qs.filter(is_public=True)
        
        return qs


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_ai_description(request):
    """Generiert KI-Beschreibung mit Groq API"""
    try:
        from groq import Groq
    except ImportError:
        return Response(
            {"error": "Groq package not installed. Run: pip install groq"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    content_type = request.data.get('type', 'pitch')
    keywords = request.data.get('keywords', '')
    tone = request.data.get('tone', 'professional')
    
    if not keywords:
        return Response(
            {"error": "Stichwörter sind erforderlich"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    api_key = getattr(settings, 'GROQ_API_KEY', None)
    if not api_key:
        return Response(
            {"error": "GROQ_API_KEY not configured in settings"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    tone_map = {
        'professional': 'professionell und überzeugend',
        'creative': 'kreativ und einzigartig',
        'technical': 'technisch detailliert und präzise'
    }
    tone_desc = tone_map.get(tone, 'professionell')
    
    if content_type == 'event':
        prompt = f"""Schreibe eine ansprechende Event-Beschreibung auf Deutsch. 
Die Beschreibung soll {tone_desc} sein.
Stichworte: {keywords}

Schreibe 2-3 Sätze, die klar erklären worum es geht und warum Teilnehmer kommen sollten.
Antworte NUR mit der Beschreibung, ohne zusätzliche Kommentare."""
    else:  # pitch
        prompt = f"""Schreibe eine überzeugende Pitch-Beschreibung für ein Startup auf Deutsch.
Die Beschreibung soll {tone_desc} sein.
Stichworte: {keywords}

Schreibe 2-3 Sätze, die das Problem, die Lösung und den Mehrwert klar kommunizieren.
Antworte NUR mit der Beschreibung, ohne zusätzliche Kommentare."""
    
    try:
        # Groq API aufrufen
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein Experte für Marketing-Texte und Startup-Pitches. Du schreibst prägnante, überzeugende Beschreibungen."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        description = response.choices[0].message.content.strip()
        
        return Response({
            "description": description
        })
        
    except Exception as e:
        return Response(
            {"error": f"AI generation failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class SavedPitchViewSet(viewsets.ModelViewSet):
    """Watchlist-Verwaltung für Investoren"""
    serializer_class = SavedPitchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedPitch.objects.filter(user=self.request.user).select_related('pitch', 'pitch__owner')

    @action(detail=False, methods=['post'])
    def save_pitch(self, request):
        """Pitch zur Watchlist hinzufügen"""
        pitch_id = request.data.get('pitch_id')
        
        if not pitch_id:
            return Response(
                {"error": "pitch_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            pitch = Pitch.objects.get(id=pitch_id)
        except Pitch.DoesNotExist:
            return Response(
                {"error": "Pitch not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        saved_pitch, created = SavedPitch.objects.get_or_create(
            user=request.user,
            pitch=pitch
        )
        
        serializer = self.get_serializer(saved_pitch)
        
        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def unsave_pitch(self, request):
        """Pitch von Watchlist entfernen"""
        pitch_id = request.data.get('pitch_id')
        
        if not pitch_id:
            return Response(
                {"error": "pitch_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            saved_pitch = SavedPitch.objects.get(
                user=request.user,
                pitch_id=pitch_id
            )
            saved_pitch.delete()
            return Response(
                {"message": "Pitch aus gespeicherter Liste entfernt"},
                status=status.HTTP_200_OK
            )
        except SavedPitch.DoesNotExist:
            return Response(
                {"error": "Gespeicherter Pitch nicht gefunden"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def check_saved(self, request):
        """Prüft ob Pitch auf Watchlist ist"""
        pitch_id = request.query_params.get('pitch_id')
        
        if not pitch_id:
            return Response(
                {"error": "pitch_id Query-Parameter ist erforderlich"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_saved = SavedPitch.objects.filter(
            user=request.user,
            pitch_id=pitch_id
        ).exists()
        
        return Response({"saved": is_saved})


class InvestmentViewSet(viewsets.ModelViewSet):
    """Portfolio-Verwaltung für Investoren"""
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Investment.objects.filter(investor=self.request.user).select_related('pitch', 'pitch__owner')

    def perform_create(self, serializer):
        serializer.save(investor=self.request.user)

    @action(detail=False, methods=['post'])
    def invest(self, request):
        """Neue Investition erstellen"""
        pitch_id = request.data.get('pitch_id')
        amount = request.data.get('amount')
        equity_percentage = request.data.get('equity_percentage')
        
        if not pitch_id or not amount:
            return Response(
                {"error": "pitch_id und amount sind erforderlich"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            pitch = Pitch.objects.get(id=pitch_id)
        except Pitch.DoesNotExist:
            return Response(
                {"error": "Pitch not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if Investment.objects.filter(investor=request.user, pitch=pitch).exists():
            return Response(
                {"error": "Sie haben bereits in diesen Pitch investiert"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        investment = Investment.objects.create(
            investor=request.user,
            pitch=pitch,
            amount=amount,
            equity_percentage=equity_percentage,
            status='active'
        )
        
        serializer = self.get_serializer(investment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investor_kpis(request):
    """KPIs und Analytics für Investor-Dashboard"""
    user = request.user
    
    investments = Investment.objects.filter(investor=user)
    saved_pitches = SavedPitch.objects.filter(user=user)
    
    total_invested = investments.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    investment_count = investments.count()
    active_investments = investments.filter(status='active').count()
    watchlist_count = saved_pitches.count()
    
    one_week_ago = datetime.now() - timedelta(days=7)
    new_this_week = saved_pitches.filter(saved_at__gte=one_week_ago).count()
    
    avg_investment = investments.aggregate(Avg('amount'))['amount__avg'] or Decimal('0')
    
    stage_weights = {
        'Pre-Seed': 1.15,
        'Seed': 1.25,
        'Series A': 1.35, 
        'Wachstum': 1.20,  
        'Reife': 1.10
    }
    
    portfolio_growth = Decimal('0')
    if investment_count > 0:
        for inv in investments.filter(status='active'):
            stage = inv.pitch.stage or 'Seed'
            growth_factor = Decimal(str(stage_weights.get(stage, 1.20)))
            portfolio_growth += (inv.amount * growth_factor - inv.amount)
        portfolio_growth = (portfolio_growth / total_invested * 100) if total_invested > 0 else Decimal('0')
    
    projected_return = total_invested * Decimal('1.35')
    roi_forecast = Decimal('35')
    
    # Erfolgsrate
    exited_count = investments.filter(status='exited').count()
    successful_exits = investments.filter(status='exited', exit_amount__gt=0).count()
    success_rate = (successful_exits / exited_count * 100) if exited_count > 0 else Decimal('0')
    
    var_data = calculate_value_at_risk(investments)
    
    # Sector Diversifizierung
    sector_distribution = {}
    for inv in investments.filter(status='active'):
        sector = inv.pitch.sector or 'Other'
        sector_distribution[sector] = sector_distribution.get(sector, 0) + float(inv.amount)
    
    # Portfolio Concentration (Herfindahl-Hirschman Index)
    total = sum(sector_distribution.values())
    hhi = sum((value / total) ** 2 for value in sector_distribution.values()) if total > 0 else 0
    concentration_risk = 'Niedrig' if hhi < 0.15 else ('Mittel' if hhi < 0.25 else 'Hoch')
    
    # Stage Distribution
    stage_distribution = {}
    for inv in investments.filter(status='active'):
        stage = inv.pitch.stage or 'Unknown'
        stage_distribution[stage] = stage_distribution.get(stage, 0) + 1
    
    # Letzte Aktivitäten 
    recent_investments = investments.order_by('-investment_date')[:5]
    recent_activity = []
    for inv in recent_investments:
        recent_activity.append({
            'id': inv.id,
            'type': 'investment',
            'title': 'Investment getätigt',
            'startup': inv.pitch.title,
            'time': format_time_ago(inv.investment_date),
            'amount': f'{inv.amount:,.0f}€'
        })
    
    # Passende Vorschläge (Top 3 Pitches basierend auf Sektorpräferenz)
    # Ermittle meisten investierten Sektoren des Benutzers
    top_sectors = sorted(sector_distribution.items(), key=lambda x: x[1], reverse=True)[:2]
    sector_names = [s[0] for s in top_sectors] if top_sectors else []
    
    #Pitches aus bevorzugten Sektoren, in die der Benutzer noch nicht investiert hat
    invested_pitch_ids = investments.values_list('pitch_id', flat=True)
    matching_pitches = Pitch.objects.filter(
        is_public=True,
        sector__in=sector_names
    ).exclude(id__in=invested_pitch_ids)[:3]
    
    matching_suggestions = []
    for pitch in matching_pitches:
        match_score = 85 + (len(sector_names) * 5)
        matching_suggestions.append({
            'id': pitch.id,
            'title': pitch.title,
            'sector': pitch.sector,
            'stage': pitch.stage,
            'desc': pitch.desc[:150],
            'img': pitch.img.url if pitch.img else None,
            'goal': pitch.goal,
            'equity': pitch.equity,
            'matchScore': min(match_score, 98),
            'matchReason': f'Passt zu deinem {pitch.sector}-Portfolio'
        })
    
    return Response({
        'totalInvested': float(total_invested),
        'startupCount': investment_count,
        'activeStartups': active_investments,
        'watchlistCount': watchlist_count,
        'newThisWeek': new_this_week,
        'avgInvestment': float(avg_investment),
        'portfolioGrowth': float(portfolio_growth.quantize(Decimal('0.1'))),
        'roiForecast': float(roi_forecast),
        'projectedReturn': float(projected_return),
        'successRate': float(success_rate.quantize(Decimal('0.1'))),
        'successfulExits': successful_exits,
        'valueAtRisk': var_data,
        'sectorDistribution': sector_distribution,
        'concentrationRisk': concentration_risk,
        'herfindahlIndex': round(hhi, 3),
        'stageDistribution': stage_distribution,
        'recentActivity': recent_activity,
        'matchingSuggestions': matching_suggestions
    })


def calculate_value_at_risk(investments):
    """Berechnet Value at Risk (VaR) für Portfolio"""
    if not investments.exists():
        return {
            'var_95': 0,
            'var_99': 0,
            'expectedLoss': 0,
            'riskLevel': 'Niedrig'
        }
    
    #Portfolio-Wert
    total_value = sum(float(inv.current_value) for inv in investments)
    
    # Risikofaktoren basierend auf Phase
    risk_factors = {
        'Pre-Seed': 0.45,  # 45% 
        'Seed': 0.35,      # 35%
        'Series A': 0.25,  
        'Wachstum': 0.15,  
        'Reife': 0.08
    }
    
    # Berechne gewichtetes durchschnittliches Risiko
    total_invested = sum(float(inv.amount) for inv in investments)
    weighted_risk = 0
    
    for inv in investments.filter(status='active'):
        stage = inv.pitch.stage or 'Seed'
        risk = risk_factors.get(stage, 0.30)
        weight = float(inv.amount) / total_invested if total_invested > 0 else 0
        weighted_risk += risk * weight
    
    # VaR
    var_95 = total_value * weighted_risk * 1.65
    var_99 = total_value * weighted_risk * 2.33
    expected_loss = var_95 * 1.3
    
    if weighted_risk < 0.20:
        risk_level = 'Niedrig'
    elif weighted_risk < 0.35:
        risk_level = 'Mittel'
    else:
        risk_level = 'Hoch'
    
    return {
        'var_95': round(var_95, 2),
        'var_99': round(var_99, 2),
        'expectedLoss': round(expected_loss, 2),
        'riskLevel': risk_level,
        'weightedRisk': round(weighted_risk * 100, 1)
    }


def format_time_ago(dt):
    """Formatiert datetime relativ (z.B. 'vor 2 Tagen')"""
    now = datetime.now()
    if dt.tzinfo is not None:
        from django.utils import timezone
        now = timezone.now()
    
    diff = now - dt
    
    if diff.days > 30:
        return f'vor {diff.days // 30} Monat{"en" if diff.days // 30 > 1 else ""}'
    elif diff.days > 0:
        return f'vor {diff.days} Tag{"en" if diff.days > 1 else ""}'
    elif diff.seconds > 3600:
        return f'vor {diff.seconds // 3600} Stunde{"n" if diff.seconds // 3600 > 1 else ""}'
    elif diff.seconds > 60:
        return f'vor {diff.seconds // 60} Minute{"n" if diff.seconds // 60 > 1 else ""}'
    else:
        return 'Gerade eben'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_certificate_pdf(request, investment_id):
    """Generiert Aktionärszertifikat-PDF für Investition"""
    from django.http import FileResponse
    from .pdf_generator import generate_investment_certificate
    
    try:
        investment = Investment.objects.select_related('investor', 'pitch').get(id=investment_id)
        
        if investment.investor != request.user:
            return Response(
                {"error": "Sie sind nicht berechtigt, dieses Zertifikat herunterzuladen."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        pdf_buffer = generate_investment_certificate(investment)
        
        filename = f"Investify_Zertifikat_{investment.pitch.title}_{investment_id}.pdf"
        response = FileResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Investment.DoesNotExist:
        return Response(
            {"error": "Investment nicht gefunden."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": f"Fehler bei der PDF-Generierung: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
