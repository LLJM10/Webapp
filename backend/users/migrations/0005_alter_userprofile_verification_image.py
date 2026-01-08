# Manuell generiert für benutzerdefinierte upload_to-Funktion

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userprofile_is_identity_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='verification_image',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.user_verification_image_path),
        ),
    ]
