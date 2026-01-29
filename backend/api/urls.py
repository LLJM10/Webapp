from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardAnalysisViewSet,
    InvestmentPortfolioViewSet,
    dashboard_view,
    investor_analyses_list,
    dashboard_html
)

router = DefaultRouter()
router.register(r'analyses', DashboardAnalysisViewSet, basename='analysis')
router.register(r'portfolios', InvestmentPortfolioViewSet, basename='portfolio')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard-html/', dashboard_html, name='dashboard-html'),
    path('investor-analyses/', investor_analyses_list, name='investor-analyses'),
]
