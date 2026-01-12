from cryptography.fernet import Fernet
from django.conf import settings
import os


def get_encryption_key():
    """
    Hole den Verschlüsselungs-Key aus den Settings.
    """
    return settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY


def encrypt_image_file(file_path):
    """
    Verschlüsselt eine Bilddatei in-place
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
    Entschlüsselt eine verschlüsselte Bilddatei    
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


