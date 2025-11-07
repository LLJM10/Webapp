# E-Mail-Verifizierung Setup

## Implementierte Features

### Backend
1. **Neue Felder in UserProfile:**
   - `is_email_verified`: Boolean (standardmäßig False)
   - `email_verification_token`: String für den Verifizierungslink

2. **E-Mail-Versand bei Registrierung:**
   - Generiert einen sicheren Token mit `secrets.token_urlsafe(32)`
   - Sendet E-Mail mit Verifizierungslink
   - Link Format: `http://localhost:3000/verify-email?token=XXXXX`

3. **Verifizierungs-Endpoint:**
   - URL: `POST /users/verify-email/`
   - Body: `{ "token": "XXXXX" }`
   - Setzt `is_email_verified = True` bei gültigem Token

### Frontend
1. **Verifizierungsseite:** `/verify-email`
   - Liest Token aus URL-Parameter
   - Sendet POST-Request an Backend
   - Zeigt Erfolg/Fehler-Status an
   - Leitet bei Erfolg zum Login weiter

2. **Registrierungsseite angepasst:**
   - Zeigt Hinweis auf Verifizierungs-E-Mail
   - Keine automatische Weiterleitung mehr
   - Benutzer muss E-Mail bestätigen

## Migrations ausführen

```bash
# Im Webapp-Ordner:
source venv/Scripts/activate  # Windows Git Bash
# oder
. venv/bin/activate           # Linux/Mac

cd backend
python manage.py migrate users
```

## E-Mail-Konfiguration (Development)

Aktuell nutzt das System `console.EmailBackend`, d.h. E-Mails werden im Terminal ausgegeben.

**Um E-Mails zu sehen:**
1. Backend-Server starten
2. Bei Registrierung wird die E-Mail im Terminal angezeigt
3. Kopiere den Verifizierungslink aus dem Terminal
4. Öffne ihn im Browser

## Für Production (später)

In `backend/settings.py` auskommentieren und anpassen:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # oder dein Provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'noreply@investify.com'
```

## Testing

1. Registriere einen neuen Benutzer
2. Schaue im Backend-Terminal nach der E-Mail
3. Kopiere den Verifizierungslink
4. Öffne den Link im Browser
5. Die Seite zeigt "E-Mail erfolgreich verifiziert"
6. Login sollte jetzt funktionieren

## TODO (Optional)

- [ ] Login nur für verifizierte Benutzer erlauben
- [ ] "E-Mail erneut senden" Funktion
- [ ] Token-Ablaufzeit (z.B. 24 Stunden)
- [ ] Production E-Mail-Provider konfigurieren
