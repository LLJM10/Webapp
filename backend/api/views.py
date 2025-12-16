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
    Custom permission: only allow owner of an object to edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Write permissions are only allowed to the owner
        return obj.owner == request.user


class PitchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pitch model.
    - Anonymous users can list/read public pitches.
    - Authenticated users can create pitches (owner set automatically).
    - Only owner can update/delete their pitches.
    - ?mine=true filter returns only pitches of the authenticated user.
    """
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        """Set owner to the current user when creating a pitch."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionally filter queryset:
        - ?mine=true returns only user's own pitches (requires auth)
        - Otherwise returns public pitches (is_public=True) or all if staff
        """
        qs = super().get_queryset()
        
        # If user requests their own pitches
        if self.request.query_params.get('mine') in ['1', 'true', 'True']:
            if self.request.user.is_authenticated:
                return qs.filter(owner=self.request.user)
            else:
                return qs.none()  # Anonymous users have no pitches
        
        # For public listing (marketplace)
        if self.request.user.is_authenticated and self.request.user.is_staff:
            # Staff can see all pitches
            return qs
        else:
            # Public users see only public pitches
            return qs.filter(is_public=True)
        
        return qs


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event model.
    - Anonymous users can list/read public events.
    - Authenticated users can create events (owner set automatically).
    - Only owner can update/delete their events.
    - ?mine=true filter returns only events of the authenticated user.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """Set owner to the current user when creating an event."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionally filter queryset:
        - ?mine=true returns only user's own events (requires auth)
        - Otherwise returns public events (is_public=True) or all if staff
        """
        qs = super().get_queryset()
        
        # If user requests their own events
        if self.request.query_params.get('mine') in ['1', 'true', 'True']:
            if self.request.user.is_authenticated:
                return qs.filter(owner=self.request.user)
            else:
                return qs.none()  # Anonymous users have no events
        
        # For public listing (marketplace)
        if self.request.user.is_authenticated and self.request.user.is_staff:
            # Staff can see all events
            return qs
        else:
            # Public users see only public events
            return qs.filter(is_public=True)
        
        return qs


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_ai_description(request):
    """
    Generate AI description using Groq API.
    Expects: { "type": "pitch"|"event", "keywords": "...", "tone": "professional"|"creative"|"technical" }
    Returns: { "description": "..." }
    """
    try:
        from groq import Groq
    except ImportError:
        return Response(
            {"error": "Groq package not installed. Run: pip install groq"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Get request data
    content_type = request.data.get('type', 'pitch')
    keywords = request.data.get('keywords', '')
    tone = request.data.get('tone', 'professional')
    
    if not keywords:
        return Response(
            {"error": "Keywords are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if API key is configured
    api_key = getattr(settings, 'GROQ_API_KEY', None)
    if not api_key:
        return Response(
            {"error": "GROQ_API_KEY not configured in settings"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Build prompt based on type and tone
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
        # Call Groq API
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
    ViewSet for SavedPitch model.
    - Only authenticated users can save/unsave pitches.
    - Users can only see their own saved pitches.
    - Custom actions: save_pitch, unsave_pitch, check_saved
    """
    serializer_class = SavedPitchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only saved pitches of the current user."""
        return SavedPitch.objects.filter(user=self.request.user).select_related('pitch', 'pitch__owner')

    @action(detail=False, methods=['post'])
    def save_pitch(self, request):
        """
        Save a pitch for the current user.
        Expects: { "pitch_id": 123 }
        Returns: SavedPitchSerializer data or error
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
        
        # Create or get existing saved pitch
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
        Remove a saved pitch for the current user.
        Expects: { "pitch_id": 123 }
        Returns: success message or error
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
                {"message": "Pitch removed from saved list"},
                status=status.HTTP_200_OK
            )
        except SavedPitch.DoesNotExist:
            return Response(
                {"error": "Saved pitch not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def check_saved(self, request):
        """
        Check if a pitch is saved by the current user.
        Query param: ?pitch_id=123
        Returns: { "saved": true/false }
        """
        pitch_id = request.query_params.get('pitch_id')
        
        if not pitch_id:
            return Response(
                {"error": "pitch_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_saved = SavedPitch.objects.filter(
            user=request.user,
            pitch_id=pitch_id
        ).exists()
        
        return Response({"saved": is_saved})


class InvestmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Investment model.
    - Only authenticated investors can create/view investments
    - Users can only see their own investments
    - Custom action for creating investment from marketplace
    """
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only investments of the current user."""
        return Investment.objects.filter(investor=self.request.user).select_related('pitch', 'pitch__owner')

    def perform_create(self, serializer):
        """Set investor to the current user when creating an investment."""
        serializer.save(investor=self.request.user)

    @action(detail=False, methods=['post'])
    def invest(self, request):
        """
        Create a new investment from marketplace.
        Expects: { "pitch_id": 123, "amount": 50000, "equity_percentage": 5 }
        """
        pitch_id = request.data.get('pitch_id')
        amount = request.data.get('amount')
        equity_percentage = request.data.get('equity_percentage')
        
        if not pitch_id or not amount:
            return Response(
                {"error": "pitch_id and amount are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            pitch = Pitch.objects.get(id=pitch_id)
        except Pitch.DoesNotExist:
            return Response(
                {"error": "Pitch not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if already invested
        if Investment.objects.filter(investor=request.user, pitch=pitch).exists():
            return Response(
                {"error": "You have already invested in this pitch"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create investment
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
    Calculate and return KPIs for investor dashboard.
    Includes: total invested, portfolio count, watchlist, avg investment,
    portfolio growth, ROI forecast, success rate, Value at Risk, and more.
    """
    user = request.user
    
    # Get all investments
    investments = Investment.objects.filter(investor=user)
    saved_pitches = SavedPitch.objects.filter(user=user)
    
    # Basic KPIs
    total_invested = investments.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    investment_count = investments.count()
    active_investments = investments.filter(status='active').count()
    watchlist_count = saved_pitches.count()
    
    # New pitches on watchlist this week
    one_week_ago = datetime.now() - timedelta(days=7)
    new_this_week = saved_pitches.filter(saved_at__gte=one_week_ago).count()
    
    # Average investment
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
    
    # Success Rate
    exited_count = investments.filter(status='exited').count()
    successful_exits = investments.filter(status='exited', exit_amount__gt=0).count()
    success_rate = (successful_exits / exited_count * 100) if exited_count > 0 else Decimal('0')
    
    # Value at Risk (VaR) Calculation
    # Using Historical Simulation method with 95% confidence level
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
    
    # Matching suggestions (top 3 pitches based on sector preference)
    # Get user's most invested sectors
    top_sectors = sorted(sector_distribution.items(), key=lambda x: x[1], reverse=True)[:2]
    sector_names = [s[0] for s in top_sectors] if top_sectors else []
    
    # Get pitches from preferred sectors that user hasn't invested in
    invested_pitch_ids = investments.values_list('pitch_id', flat=True)
    matching_pitches = Pitch.objects.filter(
        is_public=True,
        sector__in=sector_names
    ).exclude(id__in=invested_pitch_ids)[:3]
    
    matching_suggestions = []
    for pitch in matching_pitches:
        match_score = 85 + (len(sector_names) * 5)  # Simple scoring
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
    Calculate Value at Risk (VaR) for portfolio.
    Uses simplified Historical Simulation method with 95% confidence level.
    """
    if not investments.exists():
        return {
            'var_95': 0,
            'var_99': 0,
            'expectedLoss': 0,
            'riskLevel': 'Niedrig'
        }
    
    # Calculate portfolio value
    total_value = sum(float(inv.current_value) for inv in investments)
    
    # Risk factors based on stage
    risk_factors = {
        'Pre-Seed': 0.45,  # 45% risk
        'Seed': 0.35,      # 35% risk
        'Series A': 0.25,  # 25% risk
        'Wachstum': 0.15,  # 15% risk
        'Reife': 0.08      # 8% risk
    }
    
    # Calculate weighted average risk
    total_invested = sum(float(inv.amount) for inv in investments)
    weighted_risk = 0
    
    for inv in investments.filter(status='active'):
        stage = inv.pitch.stage or 'Seed'
        risk = risk_factors.get(stage, 0.30)
        weight = float(inv.amount) / total_invested if total_invested > 0 else 0
        weighted_risk += risk * weight
    
    # VaR at 95% confidence level (1.65 standard deviations)
    var_95 = total_value * weighted_risk * 1.65
    
    # VaR at 99% confidence level (2.33 standard deviations)
    var_99 = total_value * weighted_risk * 2.33
    
    # Expected loss (average loss in worst 5% scenarios)
    expected_loss = var_95 * 1.3
    
    # Risk level classification
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
    """Format datetime as 'vor X Tagen/Stunden' """
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
