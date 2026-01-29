# Webapp - Investment Dashboard

Django-based web application with investor dashboard and role-based analytics access control.

## Features

### Dashboard Analytics
- **6 Investor-Only Analyses**: Portfolio Performance, Risk Assessment, ROI Forecast, Investment Allocation, Comparative Analysis, Extended Metrics
- **2 Public Analyses**: Market Overview, Economic Indicators
- **Role-Based Access Control**: Automatic filtering based on user roles (Investor, Regular User, Admin)

### API Endpoints
- `GET /api/dashboard-html/` - Interactive HTML dashboard
- `GET /api/investor-analyses/` - JSON list of investor-only analyses
- `GET /api/dashboard/` - Personalized dashboard (authenticated)
- `GET /api/analyses/` - Role-filtered analyses (authenticated)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Run Migrations
```bash
cd backend
python manage.py migrate
```

### 3. Populate Sample Data
```bash
python manage.py populate_dashboard
```

This creates test users:
- **Admin**: admin / admin123
- **Investor**: investor1 / investor123
- **Regular User**: user1 / user123

### 4. Start Development Server
```bash
python manage.py runserver
```

### 5. View Dashboard
Open browser to: `http://localhost:8000/api/dashboard-html/`

## Documentation

See `INVESTOR_ANALYSES.md` for detailed documentation about investor-only features.

## Question Answered

**Q**: "Zeige mir welche speziellen Analysen auf dem Dashboard nur für Investoren angezeigt werden"

**A**: The following 6 special analyses are only shown to investors:
1. Portfolio Performance Analyse
2. Risikobewertung (Risk Assessment)
3. ROI-Prognose (ROI Forecast)
4. Investitionsallokation (Investment Allocation)
5. Vergleichsanalyse (Comparative Analysis)
6. Erweiterte Kennzahlen (Extended Metrics)