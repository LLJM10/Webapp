from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet, verify_email, verify_identity

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"profiles", UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', UserViewSet.as_view({'get': 'me'})),
    path('verify-email/', verify_email, name='verify-email'),
    path('verify-identity/', verify_identity, name='verify-identity'),
]

