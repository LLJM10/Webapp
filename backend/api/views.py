from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, DashboardAnalysis, InvestmentPortfolio
from .serializers import (
    DashboardAnalysisSerializer, 
    InvestmentPortfolioSerializer
)


def dashboard_html(request):
    """
    Renders the HTML dashboard showing which analyses are investor-only.
    This is the main view to answer the question: 
    "Zeige mir welche speziellen Analysen auf dem Dashboard nur für Investoren angezeigt werden"
    """
    return render(request, 'api/dashboard.html')


class DashboardAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Dashboard Analyses.
    Automatically filters investor-only analyses based on user role.
    """
    serializer_class = DashboardAnalysisSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = DashboardAnalysis.objects.filter(is_active=True)
        
        # Check if user is an investor
        try:
            profile = user.profile
            if profile.is_investor() or profile.role == 'admin':
                # Investors and admins see all analyses
                return queryset
            else:
                # Regular users only see non-investor analyses
                return queryset.filter(investor_only=False)
        except UserProfile.DoesNotExist:
            # Users without profile only see public analyses
            return queryset.filter(investor_only=False)


class InvestmentPortfolioViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Investment Portfolios.
    Users can only access their own portfolios.
    """
    serializer_class = InvestmentPortfolioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users only see their own portfolios
        return InvestmentPortfolio.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    """
    Main dashboard endpoint that returns:
    - User profile information
    - Available analyses (filtered by role)
    - List of investor-only analyses (only for investors/admins)
    """
    user = request.user
    
    # Get user profile
    try:
        profile = user.profile
        is_investor = profile.is_investor()
        is_admin = profile.role == 'admin'
    except UserProfile.DoesNotExist:
        is_investor = False
        is_admin = False
        profile = None
    
    # Get available analyses
    if is_investor or is_admin:
        analyses = DashboardAnalysis.objects.filter(is_active=True)
    else:
        analyses = DashboardAnalysis.objects.filter(is_active=True, investor_only=False)
    
    response_data = {
        'user': {
            'username': user.username,
            'is_investor': is_investor,
            'role': profile.role if profile else 'user'
        },
        'available_analyses': DashboardAnalysisSerializer(analyses, many=True).data,
        'total_analyses': analyses.count(),
        'has_access_to_investor_features': is_investor or is_admin
    }
    
    # Only include investor-only analyses info for investors and admins
    if is_investor or is_admin:
        investor_only_analyses = DashboardAnalysis.objects.filter(
            is_active=True, 
            investor_only=True
        ).values('id', 'title', 'analysis_type', 'description')
        response_data['investor_only_analyses_info'] = list(investor_only_analyses)
    
    return Response(response_data)


@api_view(['GET'])
def investor_analyses_list(request):
    """
    Public endpoint that lists which analyses are investor-only.
    This helps answer the question: "Which special analyses are only shown to investors?"
    Note: This is intentionally public to provide transparency about available investor features.
    """
    investor_analyses = DashboardAnalysis.objects.filter(
        is_active=True,
        investor_only=True
    ).values('title', 'analysis_type', 'description')
    
    return Response({
        'message': 'Spezielle Analysen, die nur für Investoren angezeigt werden:',
        'investor_only_analyses': list(investor_analyses),
        'count': len(investor_analyses)
    })
