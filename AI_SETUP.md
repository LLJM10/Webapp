# 🤖 KI-Assistent Setup - Groq API

Die App nutzt jetzt **Groq AI** um automatisch Beschreibungen für Pitches und Events zu generieren!

## ⚡ Setup (5 Minuten)

### 1. Groq Account erstellen (kostenlos!)
1. Gehe zu: https://console.groq.com
2. Klicke auf **"Sign Up"** 
3. Melde dich an mit Google/GitHub oder Email

### 2. API Key holen
1. Nach dem Login: Links auf **"API Keys"** klicken
2. **"Create API Key"** klicken
3. Name eingeben (z.B. "Investify App")
4. Key kopieren (sieht so aus: `gsk_xxxxxxxxxxxxx`)

### 3. API Key eintragen
Öffne die Datei: `backend/.env` und füge den Key ein:

```env
# Am Ende der Datei:
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

**WICHTIG**: Ersetze `your_groq_api_key_here` mit deinem echten Key!

### 4. Backend neu starten
```bash
cd backend
python manage.py runserver
```

### 5. Frontend neu starten (falls nötig)
```bash
cd frontend
npm run dev
```

## ✨ Features

### Pitch-Beschreibung generieren
1. Dashboard → **"Neues Angebot"**
2. Bei "Kurzbeschreibung" → **"✨ KI-Assistent"** Button
3. Stichworte eingeben (z.B. "MedTech, Diagnostik-App, KI")
4. Ton wählen: Professionell / Kreativ / Technisch
5. **"Beschreibung generieren"** → Fertig!

### Event-Beschreibung generieren
1. Dashboard → **"+"** Button bei Events
2. Bei "Beschreibung" → **"✨ KI-Assistent"** Button
3. Stichworte eingeben
4. Generieren & übernehmen!

## 🎯 Was macht die KI?

Die KI erstellt automatisch:
- **Pitch-Beschreibungen**: Problem, Lösung, Mehrwert (2-3 Sätze)
- **Event-Beschreibungen**: Thema, Nutzen, Call-to-Action (2-3 Sätze)

### Beispiel:
**Input**: "MedTech, KI-Diagnostik, Früherkennung von Krebs"

**Output**: "Unsere KI-gestützte Diagnostik-Plattform revolutioniert die Früherkennung von Krebserkrankungen durch präzise Bildanalyse. Mit einer Genauigkeit von 95% unterstützen wir Ärzte bei der frühzeitigen Diagnose und retten Leben. Investiere in die Zukunft der medizinischen Diagnostik."

## 📊 Groq Limits (Free Tier)

✅ **30 Requests/Minute** - mehr als genug!
✅ **14,400 Requests/Tag**
✅ **Komplett kostenlos**
✅ **Sehr schnell** (< 1 Sekunde)

## 🔧 Technische Details

### Backend Endpoint
```
POST /api/ai/generate-description/
Headers: Authorization: Bearer <token>
Body: {
  "type": "pitch" | "event",
  "keywords": "...",
  "tone": "professional" | "creative" | "technical"
}
```

### Verwendete Modelle
- **llama-3.1-70b-versatile** (Meta Llama 3.1, sehr gut für deutsche Texte)

## 🐛 Troubleshooting

### "GROQ_API_KEY not configured"
→ Hast du den Key in `.env` eingetragen? Backend neu starten!

### "Groq package not installed"
→ Führe aus: `pip install groq`

### "API generation failed"
→ Prüfe ob dein API Key korrekt ist (keine Leerzeichen!)
→ Prüfe Internetverbindung

## 💡 Nächste Schritte (optional)

- [ ] Längere Beschreibungen generieren (max_tokens erhöhen)
- [ ] Mehrere Varianten zur Auswahl anbieten
- [ ] Beschreibung bearbeiten & neu generieren
- [ ] Weitere Sprachen (Englisch, etc.)

## 🚀 Das war's!

Jetzt kannst du Pitch- und Event-Beschreibungen mit einem Klick generieren lassen! 🎉
