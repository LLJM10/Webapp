from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

def user_verification_image_path(instance, filename):
    """
    Generiert eindeutigen Dateipfad für das Verifizierungsbild jedes Benutzers.
    Format: verification_images/user_{user_id}_verification.jpg
    """
    # Dateiendung ermitteln
    ext = filename.split('.')[-1]
    # Eindeutigen Dateinamen basierend auf User-ID erstellen
    filename = f'user_{instance.user.id}_verification.{ext}'
    return os.path.join('verification_images', filename)

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('startup', 'StartUp'), ('investor', 'Investor')], default='startup')
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    verification_image = models.ImageField(upload_to=user_verification_image_path, blank=True, null=True)
    is_identity_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=UserProfile)
def encrypt_verification_image(sender, instance, created, **kwargs):
    """Verschlüsselt Verifizierungsbilder automatisch nach dem Speichern"""
    if instance.verification_image:
        from .encryption import encrypt_image_file
        file_path = instance.verification_image.path
        if os.path.exists(file_path):
            # Prüfe ob Datei bereits verschlüsselt ist (verschlüsselte Dateien starten mit gAA...)
            with open(file_path, 'rb') as f:
                first_bytes = f.read(10)
                # Wenn Datei nicht mit JPEG/PNG Header startet, ist sie wahrscheinlich verschlüsselt
                if not (first_bytes.startswith(b'\xff\xd8\xff') or first_bytes.startswith(b'\x89PNG')):
                    return  # Bereits verschlüsselt
            
            if encrypt_image_file(file_path):
                print(f"Verifizierungsbild für User {instance.user.id} verschlüsselt")
            else:
                print(f"Fehler beim Verschlüsseln des Bildes für User {instance.user.id}")

