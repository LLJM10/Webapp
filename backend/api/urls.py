from django.urls import path, include
from .views import hello, PitchViewSet, EventViewSet, generate_ai_description
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'pitches', PitchViewSet, basename='pitch')
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('hello/', hello),
    path('', include(router.urls)),
    path('payments/', include('payments.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ai/generate-description/', generate_ai_description, name='generate_ai_description'),
]


