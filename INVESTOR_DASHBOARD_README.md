# Investor Dashboard - Dokumentation

## Übersicht

Ein modernes, visuell ansprechendes FinTech-Dashboard für Investoren mit umfassenden KPIs, Performance-Metriken und AI-gestützten Investment-Empfehlungen.

## Features

### 1. **KPI Overview Cards**
Vier zentrale Metriken mit Glow-Effekten und Trend-Indikatoren:
- **Investiertes Kapital**: Gesamtsumme aller Investments mit YoY-Wachstum
- **Portfolio Startups**: Anzahl der investierten Startups mit Aktivitätsstatus
- **Watchlist**: Gemerkute Startups mit neuen Einträgen der Woche
- **Ø Investment**: Durchschnittliches Investment pro Startup mit MoM-Trend

**Design Features:**
- Farbcodierte Icon-Wrapper mit Glow-Effekten
- Hover-Animation mit Lift-Effekt
- Gradient-Hintergründe
- Responsive Grid-Layout

### 2. **Performance Metriken**
Drei Detailkarten für tiefere Einblicke:
- **Portfolio-Wachstum**: Mini-Chart mit 6-Monats-Verlauf
- **Rendite-Forecast**: Prognostizierte Returns bis Jahresende
- **Success Rate**: Kreisdiagramm mit Erfolgsquote und Exit-Anzahl

**Design Features:**
- Animierte Bar-Charts
- SVG-Ring-Progress-Indicator
- Positive Trend-Badges

### 3. **Matching-Vorschläge (AI-basiert)**
Intelligente Investment-Empfehlungen mit:
- Match-Score (in %)
- Startup-Details (Sektor, Stage, Ziel, Equity)
- Personalisierte Match-Gründe
- Hover-Preview mit Bild-Zoom

**Interaktivität:**
- Click-to-Detail Navigation
- Card Hover-Effekte
- Responsive Grid (1-3 Spalten)

### 4. **Recent Activity Timeline**
Chronologische Aktivitätenübersicht:
- **Investment**: Grünes Icon für neue Investments
- **Watchlist**: Gelbes Icon für Watchlist-Adds
- **Message**: Blaues Icon für Nachrichten

**Features:**
- Farbcodierte Icons nach Aktivitätstyp
- Zeitstempel (relativ)
- Investment-Beträge hervorgehoben

## Technische Implementierung

### Komponenten-Struktur

```vue
<template>
  <div v-else-if="user.role === 'investor'" class="investor-dashboard">
    <div class="kpi-section">...</div>
    <div class="performance-section">...</div>
    <div class="matching-section">...</div>
    <div class="activity-section">...</div>
  </div>
</template>
```

### Datenmodell

```javascript
const investorKPIs = ref({
  // Haupt-KPIs
  totalInvested: 1200000,      // in €
  startupCount: 7,              // Anzahl Startups
  activeStartups: 7,            // Aktive Startups
  watchlistCount: 3,            // Gemerkute Pitches
  newThisWeek: 2,               // Neue Watchlist-Einträge
  avgInvestment: 171428,        // Durchschnitt pro Startup
  
  // Performance-Metriken
  portfolioGrowth: 24.5,        // in % YoY
  roiForecast: 35,              // in %
  projectedReturn: 420000,      // in €
  successRate: 71,              // in %
  successfulExits: 5,           // Anzahl Exits
  
  // Matching-Vorschläge
  matchingSuggestions: [
    {
      id: 's1',
      title: 'SmartHome Energy',
      sector: 'Energy',
      stage: 'Seed',
      desc: '...',
      img: '...',
      goal: '400k',
      equity: 8,
      matchScore: 94,
      matchReason: 'Passt zu deinem Energy-Portfolio'
    }
  ],
  
  // Aktivitäten
  recentActivity: [
    {
      id: 1,
      type: 'investment',
      title: 'Investment getätigt',
      startup: 'GreenCharge',
      time: 'vor 2 Tagen',
      amount: '150.000€'
    }
  ]
})
```

### Hilfsfunktionen

#### `formatCurrency(amount)`
Formatiert Beträge in lesbares Format:
- `>= 1M`: "1.2M€"
- `>= 1k`: "400k€"
- `< 1k`: "850€"

```javascript
function formatCurrency(amount) {
  if (amount >= 1000000) {
    return (amount / 1000000).toFixed(1) + 'M€';
  } else if (amount >= 1000) {
    return (amount / 1000).toFixed(0) + 'k€';
  }
  return amount.toLocaleString('de-DE') + '€';
}
```

#### `navigateToDetail(pitchId)`
Navigation zur Pitch-Detail-Seite:

```javascript
function navigateToDetail(pitchId) {
  const router = useRouter();
  router.push(`/detail/${pitchId}`);
}
```

## CSS-Designsystem

### Farbpalette
- **Primary Glow**: `rgba(59, 130, 246, 0.4)` - Blau
- **Accent Glow**: `rgba(94, 234, 212, 0.4)` - Türkis
- **Warning Glow**: `rgba(251, 191, 36, 0.4)` - Gelb
- **Success Glow**: `rgba(34, 197, 94, 0.4)` - Grün

### Animationen
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Verwendung:**
- KPI Section: 0.5s delay
- Performance Section: 0.6s delay
- Matching Section: 0.7s delay
- Activity Section: 0.8s delay

### Hover-Effekte
- **Cards**: `translateY(-4px)` + Box-Shadow
- **Icons**: Glow-Intensität erhöhen
- **Links**: Pfeil-Animation nach rechts

## Responsive Breakpoints

### Desktop (> 1024px)
- KPI Grid: 4 Spalten
- Performance Grid: 3 Spalten
- Matching Grid: 3 Spalten

### Tablet (641px - 1024px)
- KPI Grid: 2 Spalten
- Performance Grid: 1 Spalte
- Matching Grid: 1 Spalte

### Mobile (≤ 640px)
- KPI Grid: 1 Spalte
- Reduzierte Schriftgrößen
- Kompakteres Padding

## Integration

### Backend-Anbindung (TODO)

Das Dashboard verwendet derzeit Demo-Daten. Für die Produktion sollten folgende Endpoints implementiert werden:

```javascript
// KPI-Daten laden
async function loadInvestorKPIs() {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = localStorage.getItem('access_token');
  
  const res = await fetch(`${apiBase}/investor/kpis/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  
  if (res.ok) {
    investorKPIs.value = await res.json();
  }
}

// In onMounted() aufrufen
onMounted(async () => {
  if (user.value.role === 'investor') {
    await loadInvestorKPIs();
  }
});
```

### Django Backend (Empfehlung)

**models.py:**
```python
class InvestorPortfolio(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    startup = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    equity = models.FloatField()
    invested_at = models.DateTimeField(auto_now_add=True)
    
class InvestorActivity(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20)  # investment, watchlist, message
    startup = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**views.py:**
```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investor_kpis(request):
    investor = request.user
    
    # Portfolio Berechnungen
    portfolio = InvestorPortfolio.objects.filter(investor=investor)
    total_invested = portfolio.aggregate(Sum('amount'))['amount__sum'] or 0
    startup_count = portfolio.count()
    
    # Watchlist
    watchlist = SavedPitch.objects.filter(user=investor)
    
    # Activity
    recent_activity = InvestorActivity.objects.filter(
        investor=investor
    ).order_by('-created_at')[:10]
    
    return Response({
        'totalInvested': total_invested,
        'startupCount': startup_count,
        'watchlistCount': watchlist.count(),
        # ... weitere KPIs
    })
```

## Anpassungen & Erweiterungen

### Eigene KPI hinzufügen

1. **Datenmodell erweitern:**
```javascript
investorKPIs.value.customMetric = 12345;
```

2. **KPI-Card hinzufügen:**
```vue
<div class="kpi-card glow-card">
  <div class="kpi-icon-wrapper custom-glow">
    <svg class="kpi-icon"><!-- Icon --></svg>
  </div>
  <div class="kpi-content">
    <div class="kpi-label">Custom Metric</div>
    <div class="kpi-value">{{ investorKPIs.customMetric }}</div>
  </div>
</div>
```

3. **Farbe definieren:**
```css
.custom-glow {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(139, 92, 246, 0.2));
  box-shadow: 0 4px 24px rgba(168, 85, 247, 0.4);
}
```

### Charts integrieren

Für erweiterte Charts (z.B. Chart.js):

```bash
npm install chart.js vue-chartjs
```

```vue
<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Line } from 'vue-chartjs';
</script>
```

## Best Practices

1. **Performance**: Lazy Loading für Bilder verwenden
2. **Accessibility**: ARIA-Labels für Icons hinzufügen
3. **Dark Mode**: Bereits implementiert
4. **Daten-Caching**: LocalStorage für KPIs nutzen
5. **Error Handling**: Try-Catch bei API-Calls

## Browser-Kompatibilität

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Lizenz & Credits

- **Icons**: Heroicons (MIT License)
- **Gradient-System**: Tailwind CSS Inspiration
- **Animation**: Custom CSS Keyframes
