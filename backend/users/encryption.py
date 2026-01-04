"""
Verschlüsselungs-Utilities für Verifizierungsbilder

WICHTIG: Dies ist eine Beispiel-Implementierung. Für Produktion sollten Sie:
1. Kryptographische Schlüssel sicher verwalten (z.B. mit django-environ, AWS KMS, etc.)
2. Die Schlüssel NIEMALS im Code oder Repository speichern
3. Eine professionelle Key-Management-Lösung verwenden

Installation erforderlich:
    pip install cryptography

Verwendung:
    from .encryption import encrypt_image_file, decrypt_image_file
"""

from cryptography.fernet import Fernet
from django.conf import settings
import os


def get_encryption_key():
    """
    Hole den Verschlüsselungs-Key aus den Settings.
    
    WICHTIG: In Produktion sollte der Key NICHT in settings.py stehen!
    Verwenden Sie stattdessen:
    - Umgebungsvariablen (z.B. über django-environ)
    - AWS Secrets Manager
    - HashiCorp Vault
    - Azure Key Vault
    """
    # Fallback: Generiere einen Key (NUR für Entwicklung!)
    if not hasattr(settings, 'ENCRYPTION_KEY'):
        key = Fernet.generate_key()
        print("⚠️  WARNUNG: Kein ENCRYPTION_KEY in settings.py gefunden!")
        print(f"⚠️  Generierter temporärer Key: {key.decode()}")
        print("⚠️  Fügen Sie dies zu settings.py hinzu:")
        print(f"⚠️  ENCRYPTION_KEY = '{key.decode()}'")
        return key
    
    return settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY


def encrypt_image_file(file_path):
    """
    Verschlüsselt eine Bilddatei in-place.
    
    Args:
        file_path (str): Pfad zur Datei die verschlüsselt werden soll
    
    Returns:
        bool: True wenn erfolgreich, False bei Fehler
    """
    try:
        key = get_encryption_key()
        fernet = Fernet(key)
        
        # Lese Originaldatei
        with open(file_path, 'rb') as file:
            original_data = file.read()
        
        # Verschlüssele Daten
        encrypted_data = fernet.encrypt(original_data)
        
        # Schreibe verschlüsselte Daten zurück
        with open(file_path + '.encrypted', 'wb') as file:
            file.write(encrypted_data)
        
        # Lösche Originaldatei und benenne verschlüsselte Datei um
        os.remove(file_path)
        os.rename(file_path + '.encrypted', file_path)
        
        return True
    except Exception as e:
        print(f"Fehler beim Verschlüsseln: {e}")
        return False


def decrypt_image_file(file_path, output_path=None):
    """
    Entschlüsselt eine verschlüsselte Bilddatei.
    
    Args:
        file_path (str): Pfad zur verschlüsselten Datei
        output_path (str, optional): Pfad für entschlüsselte Datei. 
                                     Wenn None, wird in-place entschlüsselt.
    
    Returns:
        bytes: Entschlüsselte Bilddaten oder None bei Fehler
    """
    try:
        key = get_encryption_key()
        fernet = Fernet(key)
        
        # Lese verschlüsselte Datei
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        
        # Entschlüssele Daten
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Wenn output_path angegeben, speichere entschlüsselte Daten
        if output_path:
            with open(output_path, 'wb') as file:
                file.write(decrypted_data)
        
        return decrypted_data
    except Exception as e:
        print(f"Fehler beim Entschlüsseln: {e}")
        return None


def decrypt_image_to_response(file_path):
    """
    Entschlüsselt ein Bild und gibt es als HTTP-Response zurück.
    
    Verwendung in Views:
        from django.http import HttpResponse
        from .encryption import decrypt_image_to_response
        
        def serve_verification_image(request, user_id):
            file_path = f'media/verification_images/user_{user_id}_verification.jpg'
            return decrypt_image_to_response(file_path)
    """
    from django.http import HttpResponse
    
    decrypted_data = decrypt_image_file(file_path)
    
    if decrypted_data:
        # Bestimme Content-Type basierend auf Dateiendung
        if file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif file_path.endswith('.png'):
            content_type = 'image/png'
        else:
            content_type = 'application/octet-stream'
        
        return HttpResponse(decrypted_data, content_type=content_type)
    
    return HttpResponse('Image not found or decryption failed', status=404)


# Alternative: Django Signal für automatische Verschlüsselung
"""
Um Bilder automatisch nach dem Upload zu verschlüsseln, 
fügen Sie dies zu models.py hinzu:

from django.db.models.signals import post_save
from django.dispatch import receiver
from .encryption import encrypt_image_file

@receiver(post_save, sender=UserProfile)
def encrypt_verification_image(sender, instance, created, **kwargs):
    if instance.verification_image:
        file_path = instance.verification_image.path
        if os.path.exists(file_path):
            encrypt_image_file(file_path)
"""
