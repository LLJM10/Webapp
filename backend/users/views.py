from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        role = self.request.data.get('role', 'startup')
        from .models import UserProfile
        UserProfile.objects.create(user=user, role=role)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
