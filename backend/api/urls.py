from django.urls import path, include
from .views import hello, PitchViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'pitches', PitchViewSet, basename='pitch')

urlpatterns = [
    path('hello/', hello),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


