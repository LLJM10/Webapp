# E-Mail Versand Konfiguration

## Schritt 1: python-dotenv installieren

```bash
cd c:/Users/lukas/Git/Webapp
source venv/Scripts/activate
pip install python-dotenv
```

## Schritt 2: Gmail App-Passwort erstellen (empfohlen)

### Gmail Setup:
1. Gehe zu https://myaccount.google.com/
2. Wähle "Sicherheit" im linken Menü
3. Aktiviere "Bestätigung in zwei Schritten" (falls nicht schon aktiv)
4. Scrolle zu "App-Passwörter"
5. Klicke auf "App-Passwörter"
6. Wähle "E-Mail" und "Anderes Gerät"
7. Gib "Django Investify" als Namen ein
8. Kopiere das 16-stellige Passwort (Format: xxxx xxxx xxxx xxxx)

### Hinweis:
- **Verwende NICHT dein normales Gmail-Passwort!**
- App-Passwörter sind sicherer und speziell für Apps

## Schritt 3: .env Datei erstellen

Erstelle eine Datei `backend/.env` (nicht `.env.example`):

```env
# Gmail Konfiguration
EMAIL_HOST_USER=deine-email@gmail.com
EMAIL_HOST_PASSWORD=xxxxyyyyzzzzwwww
DEFAULT_FROM_EMAIL=noreply@investify.com
```

Ersetze:
- `deine-email@gmail.com` mit deiner Gmail-Adresse
- `xxxxyyyyzzzzwwww` mit dem App-Passwort (ohne Leerzeichen)

## Schritt 4: .env zu .gitignore hinzufügen

Damit deine E-Mail-Credentials nicht ins Git-Repo kommen:

```bash
echo ".env" >> backend/.gitignore
```

## Schritt 5: Backend neu starten

```bash
cd backend
python manage.py runserver
```

## Schritt 6: Testen

1. Registriere einen neuen Benutzer mit deiner echten E-Mail
2. Du solltest eine E-Mail erhalten (prüfe auch Spam-Ordner!)
3. Klicke auf den Verifizierungslink

## Alternative: Andere E-Mail-Provider

### Outlook/Hotmail:
```env
EMAIL_HOST_USER=deine-email@outlook.com
EMAIL_HOST_PASSWORD=dein-passwort
```

In `settings.py`:
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
```

### Custom SMTP Server:
```env
EMAIL_HOST_USER=deine-email@firma.de
EMAIL_HOST_PASSWORD=dein-passwort
```

In `settings.py`:
```python
EMAIL_HOST = 'smtp.firma.de'
EMAIL_PORT = 587  # oder 465 für SSL
```

## Troubleshooting

### "SMTPAuthenticationError"
- Stelle sicher, dass du ein App-Passwort verwendest (nicht dein normales Passwort)
- Prüfe, ob 2-Faktor-Authentifizierung aktiviert ist

### "SMTPServerDisconnected"
- Prüfe Firewall-Einstellungen
- Versuche Port 465 mit `EMAIL_USE_SSL = True` statt TLS

### E-Mails kommen nicht an
- Prüfe Spam-Ordner
- Prüfe Backend-Terminal auf Fehler
- Teste mit einer anderen E-Mail-Adresse

## Zurück zu Console Backend (Development)

Um wieder E-Mails im Terminal anzuzeigen, ändere in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
