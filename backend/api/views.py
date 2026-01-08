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


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hallo von Django!"})


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class IsOwnerOrReadOnly(BasePermission):
    """
    Benutzerdefinierte Berechtigung: Nur der Eigentümer darf ein Objekt bearbeiten/löschen.
    """
    def has_object_permission(self, request, view, obj):
        # Lesezugriff ist für alle Anfragen erlaubt (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Schreibzugriff nur für den Eigentümer
        return obj.owner == request.user


class PitchViewSet(viewsets.ModelViewSet):
    """
    ViewSet für Pitch-Modell.
    - Anonyme Benutzer können öffentliche Pitches lesen.
    - Authentifizierte Benutzer können Pitches erstellen (Eigentümer wird automatisch gesetzt).
    - Nur der Eigentümer kann seine Pitches aktualisieren/löschen.
    - ?mine=true Filter gibt nur Pitches des authentifizierten Benutzers zurück.
    """
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        """Setzt den Eigentümer auf den aktuellen Benutzer beim Erstellen eines Pitches."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionale Filterung des Querysets:
        - ?mine=true gibt nur eigene Pitches zurück (erfordert Authentifizierung)
        - Sonst öffentliche Pitches (is_public=True) oder alle für Staff
        """
        qs = super().get_queryset()
        
        # Wenn Benutzer seine eigenen Pitches anfordert
        if self.request.query_params.get('mine') in ['1', 'true', 'True']:
            if self.request.user.is_authenticated:
                return qs.filter(owner=self.request.user)
            else:
                return qs.none()
        
        # Für öffentliche Auflistung (Marketplace)
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return qs
        else:
            return qs.filter(is_public=True)
        
        return qs


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet für Event-Modell.
    - Anonyme Benutzer können öffentliche Events lesen.
    - Authentifizierte Benutzer können Events erstellen (Eigentümer wird automatisch gesetzt).
    - Nur der Eigentümer kann seine Events aktualisieren/löschen.
    - ?mine=true Filter gibt nur Events des authentifizierten Benutzers zurück.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """Setzt den Eigentümer auf den aktuellen Benutzer beim Erstellen eines Events."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionale Filterung des Querysets:
        - ?mine=true gibt nur eigene Events zurück (erfordert Authentifizierung)
        - Sonst öffentliche Events (is_public=True) oder alle für Staff
        """
        qs = super().get_queryset()
        
        # Wenn Benutzer seine eigenen Events anfordert
        if self.request.query_params.get('mine') in ['1', 'true', 'True']:
            if self.request.user.is_authenticated:
                return qs.filter(owner=self.request.user)
            else:
                return qs.none()  # Anonyme Benutzer haben keine Events
        
        # Für öffentliche Auflistung (Marketplace)
        if self.request.user.is_authenticated and self.request.user.is_staff:
            # Staff kann alle Events sehen
            return qs
        else:
            # Öffentliche Benutzer sehen nur öffentliche Events
            return qs.filter(is_public=True)
        
        return qs


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_ai_description(request):
    """
    Generiert KI-Beschreibung mit Groq API.
    Erwartet: { "type": "pitch"|"event", "keywords": "...", "tone": "professional"|"creative"|"technical" }
    Gibt zurück: { "description": "..." }
    """
    try:
        from groq import Groq
    except ImportError:
        return Response(
            {"error": "Groq package not installed. Run: pip install groq"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Anfragedaten abrufen
    content_type = request.data.get('type', 'pitch')
    keywords = request.data.get('keywords', '')
    tone = request.data.get('tone', 'professional')
    
    if not keywords:
        return Response(
            {"error": "Stichwörter sind erforderlich"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Prüfen ob API-Schlüssel konfiguriert ist
    api_key = getattr(settings, 'GROQ_API_KEY', None)
    if not api_key:
        return Response(
            {"error": "GROQ_API_KEY not configured in settings"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Prompt basierend auf Typ und Tonalität erstellen
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
    """
    ViewSet für SavedPitch-Modell.
    - Nur authentifizierte Benutzer können Pitches speichern/entfernen.
    - Benutzer sehen nur ihre eigenen gespeicherten Pitches.
    - Benutzerdefinierte Aktionen: save_pitch, unsave_pitch, check_saved
    """
    serializer_class = SavedPitchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Gibt nur gespeicherte Pitches des aktuellen Benutzers zurück."""
        return SavedPitch.objects.filter(user=self.request.user).select_related('pitch', 'pitch__owner')

    @action(detail=False, methods=['post'])
    def save_pitch(self, request):
        """
        Speichert einen Pitch für den aktuellen Benutzer.
        Erwartet: { "pitch_id": 123 }
        Gibt zurück: SavedPitchSerializer Daten oder Fehler
        """
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
        
        # Gespeicherten Pitch erstellen oder abrufen
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
        """
        Entfernt einen gespeicherten Pitch für den aktuellen Benutzer.
        Erwartet: { "pitch_id": 123 }
        Gibt zurück: Erfolgsmeldung oder Fehler
        """
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
        """
        Prüft ob ein Pitch vom aktuellen Benutzer gespeichert ist.
        Query-Parameter: ?pitch_id=123
        Gibt zurück: { "saved": true/false }
        """
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
    """
    ViewSet für Investment-Modell.
    - Nur authentifizierte Investoren können Investitionen erstellen/ansehen
    - Benutzer sehen nur ihre eigenen Investitionen
    - Benutzerdefinierte Aktion für Investitionen vom Marketplace
    """
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Gibt nur Investitionen des aktuellen Benutzers zurück."""
        return Investment.objects.filter(investor=self.request.user).select_related('pitch', 'pitch__owner')

    def perform_create(self, serializer):
        """Setzt den Investor auf den aktuellen Benutzer beim Erstellen einer Investition."""
        serializer.save(investor=self.request.user)

    @action(detail=False, methods=['post'])
    def invest(self, request):
        """
        Erstellt eine neue Investition vom Marketplace.
        Erwartet: { "pitch_id": 123, "amount": 50000, "equity_percentage": 5 }
        """
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
        
        # Prüfen ob bereits investiert
        if Investment.objects.filter(investor=request.user, pitch=pitch).exists():
            return Response(
                {"error": "Sie haben bereits in diesen Pitch investiert"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Investition erstellen
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
    """
    Berechnet und gibt KPIs für das Investor-Dashboard zurück.
    Enthält: Gesamtinvestition, Portfolio-Anzahl, Watchlist, Durchschnittsinvestition,
    Portfolio-Wachstum, ROI-Prognose, Erfolgsquote, Value at Risk und mehr.
    """
    user = request.user
    
    # Alle Investitionen abrufen
    investments = Investment.objects.filter(investor=user)
    saved_pitches = SavedPitch.objects.filter(user=user)
    
    # Basis-KPIs
    total_invested = investments.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    investment_count = investments.count()
    active_investments = investments.filter(status='active').count()
    watchlist_count = saved_pitches.count()
    
    # Neue Pitches auf der Watchlist diese Woche
    one_week_ago = datetime.now() - timedelta(days=7)
    new_this_week = saved_pitches.filter(saved_at__gte=one_week_ago).count()
    
    # Durchschnittliche Investition
    avg_investment = investments.aggregate(Avg('amount'))['amount__avg'] or Decimal('0')
    
    # Portfolio growth (simulated based on stage distribution)
    stage_weights = {
        'Pre-Seed': 1.15,  # 15% growth assumption
        'Seed': 1.25,      # 25% growth
        'Series A': 1.35,  # 35% growth
        'Wachstum': 1.20,  # 20% growth
        'Reife': 1.10      # 10% growth
    }
    
    portfolio_growth = Decimal('0')
    if investment_count > 0:
        for inv in investments.filter(status='active'):
            stage = inv.pitch.stage or 'Seed'
            growth_factor = Decimal(str(stage_weights.get(stage, 1.20)))
            portfolio_growth += (inv.amount * growth_factor - inv.amount)
        portfolio_growth = (portfolio_growth / total_invested * 100) if total_invested > 0 else Decimal('0')
    
    # ROI Forecast (projected return)
    projected_return = total_invested * Decimal('1.35')  # 35% ROI assumption
    roi_forecast = Decimal('35')
    
    # Erfolgsrate
    exited_count = investments.filter(status='exited').count()
    successful_exits = investments.filter(status='exited', exit_amount__gt=0).count()
    success_rate = (successful_exits / exited_count * 100) if exited_count > 0 else Decimal('0')
    
    # Value at Risk (VaR) Berechnung
    # Verwendet Historical Simulation-Methode mit 95% Konfidenzniveau
    var_data = calculate_value_at_risk(investments)
    
    # Sector Diversification
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
    
    # Recent activity
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
    # Ermittle die am meisten investierten Sektoren des Benutzers
    top_sectors = sorted(sector_distribution.items(), key=lambda x: x[1], reverse=True)[:2]
    sector_names = [s[0] for s in top_sectors] if top_sectors else []
    
    # Hole Pitches aus bevorzugten Sektoren, in die der Benutzer noch nicht investiert hat
    invested_pitch_ids = investments.values_list('pitch_id', flat=True)
    matching_pitches = Pitch.objects.filter(
        is_public=True,
        sector__in=sector_names
    ).exclude(id__in=invested_pitch_ids)[:3]
    
    matching_suggestions = []
    for pitch in matching_pitches:
        match_score = 85 + (len(sector_names) * 5)  # Einfache Bewertung
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
    """
    Berechnet Value at Risk (VaR) für das Portfolio.
    Verwendet vereinfachte Historische Simulationsmethode mit 95% Konfidenzniveau.
    """
    if not investments.exists():
        return {
            'var_95': 0,
            'var_99': 0,
            'expectedLoss': 0,
            'riskLevel': 'Niedrig'
        }
    
    # Berechne Portfolio-Wert
    total_value = sum(float(inv.current_value) for inv in investments)
    
    # Risikofaktoren basierend auf Phase
    risk_factors = {
        'Pre-Seed': 0.45,  # 45% risk
        'Seed': 0.35,      # 35% risk
        'Series A': 0.25,  # 25% risk
        'Wachstum': 0.15,  # 15% risk
        'Reife': 0.08      # 8% risk
    }
    
    # Berechne gewichtetes durchschnittliches Risiko
    total_invested = sum(float(inv.amount) for inv in investments)
    weighted_risk = 0
    
    for inv in investments.filter(status='active'):
        stage = inv.pitch.stage or 'Seed'
        risk = risk_factors.get(stage, 0.30)
        weight = float(inv.amount) / total_invested if total_invested > 0 else 0
        weighted_risk += risk * weight
    
    # VaR bei 95% Konfidenzniveau (1.65 Standardabweichungen)
    var_95 = total_value * weighted_risk * 1.65
    
    # VaR bei 99% Konfidenzniveau (2.33 Standardabweichungen)
    var_99 = total_value * weighted_risk * 2.33
    
    # Erwarteter Verlust (durchschnittlicher Verlust in den schlechtesten 5% Szenarien)
    expected_loss = var_95 * 1.3
    
    # Risikoebenen-Klassifizierung
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
    """Formatiert datetime als 'vor X Tagen/Stunden'."""
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
    """
    Generiert und lädt Aktionärszertifikat-PDF für eine Investition herunter.
    GET /api/investments/<id>/certificate/
    """
    from django.http import FileResponse
    from .pdf_generator import generate_investment_certificate
    
    try:
        # Investition abrufen und Eigentümerschaft prüfen
        investment = Investment.objects.select_related('investor', 'pitch').get(id=investment_id)
        
        # Prüfen ob Benutzer diese Investition besitzt
        if investment.investor != request.user:
            return Response(
                {"error": "Sie sind nicht berechtigt, dieses Zertifikat herunterzuladen."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # PDF generieren
        pdf_buffer = generate_investment_certificate(investment)
        
        # Als Datei-Antwort zurückgeben
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
