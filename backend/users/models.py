from django.db import models
from django.contrib.auth.models import User
import os

def user_verification_image_path(instance, filename):
    """
    Generate unique file path for each user's verification image.
    Format: verification_images/user_{user_id}_verification.jpg
    """
    # Get file extension
    ext = filename.split('.')[-1]
    # Create unique filename based on user ID
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

