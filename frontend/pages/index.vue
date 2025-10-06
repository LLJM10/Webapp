<template>
<section id="page-landing">
<div class="hero">
<div>
<h1 class="large">Investiere in die Innovation von morgen — mit <span style="color:var(--accent)">investify</span>.</h1>
<p class="lead">Eine sichere B2B-Plattform, die Gründer & verifizierte Investoren zusammenbringt. Pitch hochladen, Investoren finden, Co-Investments organisieren und Wachstum skalieren — alles an einem Ort.</p>
<div class="cta-row">
<NuxtLink to="/profile" class="btn primary">Jetzt Demo-Profil ansehen</NuxtLink>
<NuxtLink to="/market" class="btn ghost">Marktplatz vorschau</NuxtLink>
</div>
<div class="grid-3">
<FeatureCard title="Pitching & Dokumente" desc="Strukturierte Pitch-Profile mit Video, Cap Table und KPIs für bessere Entscheidungen." />
<FeatureCard title="Verifiziertes Netzwerk" desc="KYC & OpenVerify Workflows, Co-Investor Matching und Due Diligence Tools." />
<FeatureCard title="Intelligente Matches" desc="AI-gestützte Empfehlungen für Deals, basierend auf Präferenzen & Track Record." />
</div>
<div style="margin-top:20px;display:flex;gap:12px;align-items:center">
<div class="badge">Demo & Mock Data</div>
<div class="muted">Seiten vollständig im Look gefüllt — klick dich durch.</div>
</div>
</div>
<aside>
<div class="hero-card">
<div style="display:flex;justify-content:space-between;align-items:center">
<div>
<div class="muted">Top-Pitch</div>
<strong>SmartHome Energy</strong>
</div>
<div class="tag">AI · Energy</div>
</div>
<img src="https://picsum.photos/seed/hero/900/520" alt="mockup" style="margin-top:12px;border-radius:8px" />
<div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px">
<div class="muted">Funding Ziel: 400k €</div>
<div class="muted">Anteile: 8%</div>
</div>
</div>
<div style="margin-top:12px" class="card">
<strong>Unsere Versprechen</strong>
<div class="muted" style="margin-top:8px">Kuratiert, transparent und datengetrieben — vorbereitet für echte Investitionsprozesse.</div>
</div>
</aside>
</div>
<div style="margin-top:28px">
<h2>Marktplatz — Vorschau</h2>
<p class="muted">Eine Auswahl interessanter Pitches. Voller Zugriff im Marktplatz.</p>
<div class="list">
<PitchCard v-for="s in previewStartups" :key="s.id" :pitch="s" />
</div>
</div>
</section>
</template>
<script setup>
// Demo-Daten (Im echten Nuxt würden diese aus einem Store/API geladen)
const startups = [
 { id:'s1', title:'SmartHome Energy', sector:'Energy', stage:'Seed', desc:'Dezentrale Energieoptimierung für Privathaushalte mittels Edge-AI und Lastverschiebung.', img:'https://picsum.photos/seed/s1/900/480', kpis:{revenue:'420k€ TTM', growth:'+72% YoY', customers:'1.2k'}, traction:'Pilot in 3 Städten', market:'DACH', goal:'400k€', equity:'8%'},
 { id:'s2', title:'GreenCharge', sector:'AI', stage:'Series A', desc:'Batterie-Management für EV-Flotten mit optimierter Ladeplanung und Flotten-Analytics.', img:'https://picsum.photos/seed/s2/900/480', kpis:{revenue:'1.1M€ TTM', growth:'+120% YoY', customers:'35 fleets'}, traction:'Verträge mit 2 großen Flottenbetreibern', market:'EU', goal:'2.5M€', equity:'12%'},
 { id:'s3', title:'Medico', sector:'Health', stage:'Seed', desc:'Telehealth für chronisch Kranke mit KI-Triage & Adhärenz-Programmen.', img:'https://picsum.photos/seed/s3/900/480', kpis:{revenue:'320k€ TTM', growth:'+48% YoY', customers:'4k'}, traction:'Pilot mit Klinikgruppe; 85% Retention', market:'EU', goal:'500k€', equity:'6%'},
 { id:'s4', title:'OrbitSense', sector:'SpaceTech', stage:'Pre-Seed', desc:'Low-cost Sensor-Satellites zur Erfassung von Luftqualität & Emissionen.', img:'https://picsum.photos/seed/s4/900/480', kpis:{revenue:'—', growth:'—', customers:'2 research projects'}, traction:'1 Test-Sat in LEO erfolgreich', market:'Global', goal:'800k€', equity:'15%'}
];
// Zeige die ersten 3 Startups für die Vorschau
const previewStartups = startups.slice(0, 3);
</script>