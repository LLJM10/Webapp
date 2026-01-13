Voraussetzungen

- Git (https://git-scm.com/downloads)
- Python 3.10+ (https://www.python.org/downloads/)
- Node.js 18+ (https://nodejs.org/)

Setup Anleitung

1. Repository klonen
   git clone https://github.com/LLJM10/Webapp.git
   cd Webapp
   
   Für spezifischen Branch:
   git clone https://github.com/LLJM10/Webapp.git -b branch-name


2. Virtuelle Umgebung erstellen und aktivieren
   python -m venv venv
   
   Windows:
   source venv/Scripts/activate
   
   Linux/Mac:
   source venv/bin/activate


3. Abhängigkeiten installieren
   cd backend
   pip install -r requirements.txt


4. Umgebungsvariablen einrichten

   .env Datei im backend/ Ordner erstellen mit folgendem Inhalt:

# Email Credentials
EMAIL_HOST_USER=deine-email@gmail.com
EMAIL_HOST_PASSWORD=dein-app-passwort
DEFAULT_FROM_EMAIL=noreply@investify.com

# Groq API Key 
GROQ_API_KEY=dein-groq-api-key

# PayPal Credentials
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=deine-paypal-client-id
PAYPAL_CLIENT_SECRET=dein-paypal-client-secret
PAYPAL_WEBHOOK_ID=optional

# Verschlüsselungs Key
ENCRYPTION_KEY=generiere-einen-fernet-key

   Fernet Key generieren:
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"


5. Datenbank migrieren
   python manage.py makemigrations
   python manage.py migrate


6. Backend starten
   python manage.py runserver
   
   Backend läuft auf: http://127.0.0.1:8000
   Admin Panel: http://127.0.0.1:8000/admin


7. Frontend Setup (neues Terminal öffnen)
   cd frontend
   npm install


8. Frontend starten
   npm run dev
   
   Frontend läuft jetzt auf: http://localhost:3000




