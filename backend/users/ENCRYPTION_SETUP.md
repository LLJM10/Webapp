# Bild-Verschlüsselung Setup

## ✅ Was wurde implementiert

### 1. Eindeutige Dateinamen pro User
- ✅ Dateiformat: `verification_images/user_{user_id}_verification.jpg`
- ✅ Alte Bilder werden automatisch gelöscht beim neuen Upload
- ✅ Jeder User hat maximal EIN Verifizierungsbild

### 2. Validierung
- ✅ Nur JPEG und PNG erlaubt
- ✅ Maximale Dateigröße: 5MB
- ✅ Content-Type Prüfung

### 3. Sicherheit
- ✅ Alte Dateien werden physisch gelöscht
- ✅ Authentifizierung erforderlich (JWT Token)

---

## 🔐 Verschlüsselung aktivieren (Optional)

### Schritt 1: Cryptography installieren

```bash
pip install cryptography
```

### Schritt 2: Verschlüsselungs-Key generieren

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**Beispiel-Output:**
```
mZJTvHKp8YXq2w5s8C3zN4vF6dGhJkL9pRtYuIoP1aQ=
```

### Schritt 3: Key in settings.py einfügen

**backend/backend/settings.py:**

```python
# Verschlüsselung für Verifizierungsbilder
# ⚠️ WICHTIG: In Produktion über Umgebungsvariablen laden!
ENCRYPTION_KEY = 'mZJTvHKp8YXq2w5s8C3zN4vF6dGhJkL9pRtYuIoP1aQ='  # Ihr generierter Key
```

**Für Produktion (mit Umgebungsvariablen):**

```python
import os
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
```

### Schritt 4: Automatische Verschlüsselung aktivieren

**Option A: In models.py (empfohlen)**

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .encryption import encrypt_image_file
import os

@receiver(post_save, sender=UserProfile)
def encrypt_verification_image(sender, instance, created, **kwargs):
    """Verschlüsselt Verifizierungsbilder automatisch nach dem Speichern"""
    if instance.verification_image:
        file_path = instance.verification_image.path
        if os.path.exists(file_path):
            encrypt_image_file(file_path)
            print(f"✓ Bild für User {instance.user.id} verschlüsselt")
```

**Option B: In views.py (manuelle Kontrolle)**

```python
from .encryption import encrypt_image_file

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_identity(request):
    # ... (bestehender Code)
    
    profile.verification_image = verification_image
    profile.save()
    
    # Verschlüssele das Bild nach dem Speichern
    if profile.verification_image:
        encrypt_image_file(profile.verification_image.path)
    
    return Response(...)
```

### Schritt 5: Bilder entschlüsseln zum Anzeigen

**Neue View zum Anzeigen verschlüsselter Bilder:**

```python
from django.http import HttpResponse
from .encryption import decrypt_image_file
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

@api_view(['GET'])
@permission_classes([IsAdminUser])  # Nur Admins dürfen Bilder sehen
def view_verification_image(request, user_id):
    """Zeigt verschlüsseltes Verifizierungsbild"""
    try:
        profile = UserProfile.objects.get(user_id=user_id)
        if not profile.verification_image:
            return HttpResponse('Kein Bild vorhanden', status=404)
        
        file_path = profile.verification_image.path
        decrypted_data = decrypt_image_file(file_path)
        
        if decrypted_data:
            return HttpResponse(decrypted_data, content_type='image/jpeg')
        return HttpResponse('Entschlüsselung fehlgeschlagen', status=500)
    except UserProfile.DoesNotExist:
        return HttpResponse('User nicht gefunden', status=404)
```

**In urls.py:**

```python
from .views import view_verification_image

urlpatterns = [
    # ... bestehende URLs
    path('verification-image/<int:user_id>/', view_verification_image, name='view-verification-image'),
]
```

---

## 🔒 Sicherheitshinweise

### ⚠️ Key-Management in Produktion

**NIEMALS** den Verschlüsselungs-Key im Code oder Git speichern!

**Sichere Optionen:**

1. **Umgebungsvariablen** (für kleinere Projekte):
   ```python
   import os
   ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
   ```

2. **Django-Environ** (empfohlen):
   ```bash
   pip install django-environ
   ```
   ```python
   import environ
   env = environ.Env()
   ENCRYPTION_KEY = env('ENCRYPTION_KEY')
   ```

3. **AWS Secrets Manager** (für AWS):
   ```python
   import boto3
   client = boto3.client('secretsmanager')
   secret = client.get_secret_value(SecretId='prod/encryption/key')
   ENCRYPTION_KEY = secret['SecretString']
   ```

4. **Azure Key Vault** (für Azure)
5. **HashiCorp Vault** (Enterprise)

### 🔐 Weitere Sicherheitsmaßnahmen

**In settings.py hinzufügen:**

```python
# Nur über HTTPS zugreifen (Produktion)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS aktivieren
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content Security Policy
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
```

---

## 📊 Verschlüsselung vs. Nicht-Verschlüsselt

| Aspekt | Ohne Verschlüsselung | Mit Verschlüsselung |
|--------|---------------------|---------------------|
| Dateiname | `user_123_verification.jpg` | `user_123_verification.jpg` |
| Dateigröße | ~500 KB | ~670 KB (+33%) |
| Lesbar | Ja, direkt | Nein, nur mit Key |
| Performance | Schnell | Etwas langsamer |
| Sicherheit | Basis | Hoch |
| Komplexität | Niedrig | Mittel |

---

## 🧪 Testen

### Verschlüsselung testen:

```bash
cd backend
python manage.py shell
```

```python
from users.encryption import encrypt_image_file, decrypt_image_file

# Teste Verschlüsselung
file_path = 'media/verification_images/user_1_verification.jpg'
encrypt_image_file(file_path)
print("✓ Verschlüsselt")

# Teste Entschlüsselung
data = decrypt_image_file(file_path)
print(f"✓ Entschlüsselt: {len(data)} bytes")
```

---

## 🚀 Migration bestehender Bilder

Falls bereits unverschlüsselte Bilder existieren:

```python
# backend/users/management/commands/encrypt_existing_images.py
from django.core.management.base import BaseCommand
from users.models import UserProfile
from users.encryption import encrypt_image_file
import os

class Command(BaseCommand):
    help = 'Verschlüsselt alle bestehenden Verifizierungsbilder'

    def handle(self, *args, **kwargs):
        profiles = UserProfile.objects.exclude(verification_image='')
        
        for profile in profiles:
            if profile.verification_image:
                file_path = profile.verification_image.path
                if os.path.exists(file_path):
                    encrypt_image_file(file_path)
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ User {profile.user.id} verschlüsselt')
                    )
```

**Ausführen:**

```bash
python manage.py encrypt_existing_images
```

---

## ❓ FAQ

**Q: Werden die Bilder bei jedem Upload verschlüsselt?**  
A: Ja, wenn die automatische Verschlüsselung aktiviert ist (siehe Schritt 4).

**Q: Kann ich verschlüsselte Bilder im Admin-Panel sehen?**  
A: Nein, nicht direkt. Sie müssen eine spezielle View erstellen (siehe Schritt 5).

**Q: Was passiert wenn ich den Key verliere?**  
A: Alle verschlüsselten Bilder sind permanent verloren! Backup des Keys ist essentiell.

**Q: Ist die Verschlüsselung DSGVO-konform?**  
A: Verschlüsselung ist ein wichtiger Schritt, aber DSGVO erfordert mehr (Zugriffskontrollen, Löschkonzept, Dokumentation, etc.).

**Q: Performance-Impact?**  
A: Minimal. Die Verschlüsselung dauert ~50-100ms pro Bild.
