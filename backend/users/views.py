from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import secrets
import os
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_email(self, request):
        """Update user's email address"""
        user = request.user
        new_email = request.data.get('email')
        
        if not new_email:
            return Response(
                {'error': 'E-Mail Adresse erforderlich'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if email already exists
        if User.objects.filter(email=new_email).exclude(id=user.id).exists():
            return Response(
                {'error': 'Diese E-Mail Adresse wird bereits verwendet'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update email
        user.email = new_email
        user.save()
        
        return Response(
            {'message': 'E-Mail Adresse erfolgreich aktualisiert', 'email': new_email}, 
            status=status.HTTP_200_OK
        )
    
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_identity(request):
    """Handle identity verification with uploaded image"""
    try:
        user = request.user
        profile = UserProfile.objects.get(user=user)
        
        if 'verification_image' not in request.FILES:
            return Response(
                {'error': 'Bitte laden Sie ein Bild hoch'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        verification_image = request.FILES['verification_image']
        
        # Validierung: Dateityp prüfen
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
        if verification_image.content_type not in allowed_types:
            return Response(
                {'error': 'Nur JPEG und PNG Bilder sind erlaubt'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validierung: Dateigröße prüfen (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if verification_image.size > max_size:
            return Response(
                {'error': 'Bild darf maximal 5MB groß sein'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Lösche altes Verifizierungsbild falls vorhanden
        if profile.verification_image:
            # Lösche physische Datei
            if os.path.isfile(profile.verification_image.path):
                os.remove(profile.verification_image.path)
        
        # Speichere neues Verifizierungsbild
        # Der Dateiname wird automatisch durch user_verification_image_path generiert
        profile.verification_image = verification_image
        profile.save()
        
        return Response(
            {'message': 'Verifizierungsbild erfolgreich hochgeladen. Unser Team wird es überprüfen.'},
            status=status.HTTP_200_OK
        )
    
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'Benutzerprofil nicht gefunden'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Fehler beim Hochladen: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_verification_image(request, user_id):
    """
    Zeigt verschlüsseltes Verifizierungsbild.
    """
    try:
        profile = UserProfile.objects.get(user_id=user_id)
        
        # Nur eigenes Bild oder Admin darf zugreifen
        if request.user.id != user_id and not request.user.is_staff:
            return HttpResponse('Keine Berechtigung', status=403)
        
        if not profile.verification_image:
            return HttpResponse('Kein Bild vorhanden', status=404)
        
        file_path = profile.verification_image.path
        
        # Versuche Bild zu entschlüsseln
        from .encryption import decrypt_image_file
        decrypted_data = decrypt_image_file(file_path)
        
        if decrypted_data:
            # Erkenne Content-Type basierend auf Dateiendung
            if file_path.lower().endswith('.png'):
                content_type = 'image/png'
            else:
                content_type = 'image/jpeg'
            return HttpResponse(decrypted_data, content_type=content_type)
        
        return HttpResponse('Entschlüsselung fehlgeschlagen', status=500)
    
    except UserProfile.DoesNotExist:
        return HttpResponse('User nicht gefunden', status=404)
    except Exception as e:
        return HttpResponse(f'Fehler: {str(e)}', status=500)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

