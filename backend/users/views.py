from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import secrets
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        role = self.request.data.get('role', 'startup')
        
        # Generate verification token
        verification_token = secrets.token_urlsafe(32)
        
        # Create UserProfile with verification token
        profile = UserProfile.objects.create(
            user=user, 
            role=role,
            email_verification_token=verification_token,
            is_email_verified=False
        )
        
        # Send verification email
        verification_url = f"http://localhost:3000/verify-email?token={verification_token}"
        
        # Debug: Print email settings (remove in production!)
        print(f"=== EMAIL DEBUG ===")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
        print(f"Sending email to: {user.email}")
        print(f"==================")
        
        try:
            send_mail(
                subject='Verifiziere deine E-Mail-Adresse',
                message=f'Hallo {user.username},\n\nBitte klicke auf den folgenden Link, um deine E-Mail-Adresse zu verifizieren:\n\n{verification_url}\n\nVielen Dank!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print(f"Verification email sent to {user.email}")
        except Exception as e:
            print(f"Error sending email: {e}")

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.data.get('token')
    
    if not token:
        return Response({'error': 'Token erforderlich'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        profile = UserProfile.objects.get(email_verification_token=token)
        
        if profile.is_email_verified:
            return Response({'message': 'E-Mail bereits verifiziert'}, status=status.HTTP_200_OK)
        
        profile.is_email_verified = True
        profile.email_verification_token = None  # Token nach Verwendung löschen
        profile.save()
        
        return Response({'message': 'E-Mail erfolgreich verifiziert'}, status=status.HTTP_200_OK)
    
    except UserProfile.DoesNotExist:
        return Response({'error': 'Ungültiger Token'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

