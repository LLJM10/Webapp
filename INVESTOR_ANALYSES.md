# Dashboard Analytics - Investor-Only Features

## Übersicht / Overview

Diese Dokumentation beschreibt, welche speziellen Analysen auf dem Dashboard nur für Investoren angezeigt werden.

This documentation describes which special analyses on the dashboard are only displayed for investors.

## Investoren-exklusive Analysen / Investor-Only Analyses

Die folgenden **6 Analysen** sind nur für Benutzer mit der Rolle "Investor" sichtbar:

The following **6 analyses** are only visible to users with the "Investor" role:

### 1. Portfolio Performance Analyse
- **Typ**: Portfolio Performance Analysis
- **Beschreibung**: Detaillierte Analyse der Portfolio-Performance mit historischen Daten
- **Enthält**: Renditen, Sharpe Ratio, Volatilität, Top-Performer

### 2. Risikobewertung
- **Typ**: Risk Assessment
- **Beschreibung**: Umfassende Risikobewertung mit VaR und Stress-Tests
- **Enthält**: Value-at-Risk, Expected Shortfall, Risk Grade, Stress-Test-Ergebnisse

### 3. ROI-Prognose
- **Typ**: ROI Forecast
- **Beschreibung**: Erwartete Rendite-Prognosen für die nächsten 12 Monate
- **Enthält**: 12-Monats-Prognose, Konfidenzlevel, Best-Case/Worst-Case-Szenarien

### 4. Investitionsallokation
- **Typ**: Investment Allocation
- **Beschreibung**: Optimierte Asset-Allocation-Strategie
- **Enthält**: Verteilung über Aktien, Anleihen, Immobilien, Rohstoffe

### 5. Vergleichsanalyse
- **Typ**: Comparative Analysis
- **Beschreibung**: Vergleich mit Benchmark-Indizes und Peer-Portfolios
- **Enthält**: Performance vs. S&P 500, DAX, Peer-Average, Ranking

### 6. Erweiterte Kennzahlen
- **Typ**: Portfolio Performance
- **Beschreibung**: Detaillierte Performance-Metriken für Investoren
- **Enthält**: Alpha, Beta, Treynor Ratio, Information Ratio, Maximum Drawdown

## Öffentliche Analysen / Public Analyses

Diese Analysen sind für **alle Benutzer** sichtbar:

These analyses are visible to **all users**:

1. **Marktübersicht** - Allgemeine Markttrends und Übersichten
2. **Wirtschaftsindikatoren** - Wichtige wirtschaftliche Kennzahlen

## Zugriffskontrolle / Access Control

### Investor-Rolle
- ✅ Zugriff auf alle öffentlichen Analysen
- ✅ Zugriff auf alle 6 investoren-exklusiven Analysen
- ✅ Zugriff auf Investment-Portfolios

### Regular User-Rolle
- ✅ Zugriff auf alle öffentlichen Analysen
- ❌ Kein Zugriff auf investoren-exklusive Analysen

### Admin-Rolle
- ✅ Zugriff auf alle Analysen
- ✅ Verwaltung aller Benutzer und Daten

## API-Endpunkte / API Endpoints

### Dashboard HTML View
```
GET /api/dashboard-html/
```
Zeigt eine HTML-Seite mit allen investoren-exklusiven Analysen.

### Investor Analyses List (JSON)
```
GET /api/investor-analyses/
```
Gibt eine JSON-Liste aller investoren-exklusiven Analysen zurück.

**Beispiel-Response**:
```json
{
  "message": "Spezielle Analysen, die nur für Investoren angezeigt werden:",
  "investor_only_analyses": [
    {
      "title": "Portfolio Performance Analyse",
      "analysis_type": "portfolio_performance",
      "description": "Detaillierte Analyse der Portfolio-Performance mit historischen Daten"
    },
    ...
  ],
  "count": 6
}
```

### Dashboard API (Authenticated)
```
GET /api/dashboard/
```
Erfordert Authentifizierung. Gibt personalisierte Dashboard-Daten basierend auf der Benutzerrolle zurück.

### Analyses ViewSet
```
GET /api/analyses/
```
Erfordert Authentifizierung. Filtert automatisch Analysen basierend auf der Benutzerrolle.

## Test-Benutzer / Test Users

Die Datenbank wurde mit folgenden Test-Benutzern befüllt:

| Username | Passwort | Rolle | Zugriff |
|----------|----------|-------|---------|
| admin | admin123 | Admin | Alle Analysen |
| investor1 | investor123 | Investor | Alle Analysen |
| user1 | user123 | Regular User | Nur öffentliche Analysen |

## Datenbank initialisieren / Initialize Database

Um die Datenbank mit Beispieldaten zu befüllen:

```bash
cd backend
source ../venv/bin/activate
python manage.py populate_dashboard
```

## Technische Details / Technical Details

### Models
- `UserProfile`: Erweitert Django User mit Rollen (investor, user, admin)
- `DashboardAnalysis`: Speichert Analysen mit `investor_only` Flag
- `InvestmentPortfolio`: Investment-Portfolios für Investoren

### Views
- `DashboardAnalysisViewSet`: Filtert Analysen basierend auf Benutzerrolle
- `dashboard_html()`: Rendert HTML-Dashboard
- `investor_analyses_list()`: Gibt Liste aller investoren-exklusiven Analysen zurück

### Security
- Alle sensiblen Endpunkte erfordern Authentifizierung
- Role-based Access Control (RBAC) implementiert
- Automatische Filterung basierend auf Benutzerrolle
