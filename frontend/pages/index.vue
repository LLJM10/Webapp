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
<div class="flex gap-12 mt-20 align-center">
  <div class="badge">Demo & Mock Data</div>
  <div class="muted">Seiten vollständig im Look gefüllt — klick dich durch.</div>
</div>
</div>
<aside>
<div class="hero-card">
  <div class="flex-between">
    <div>
      <div class="muted">Top-Pitch</div>
      <strong>SmartHome Energy</strong>
    </div>
    <div class="tag">AI · Energy</div>
  </div>
  <img src="https://picsum.photos/seed/hero/900/520" alt="mockup" class="mt-12 img-round-8" />
  <div class="flex-between mt-10">
    <div class="muted">Funding Ziel: 400k €</div>
    <div class="muted">Anteile: 8%</div>
  </div>
</div>
<div class="card mt-12">
  <strong>Unsere Versprechen</strong>
  <div class="muted mt-8">Kuratiert, transparent und datengetrieben — vorbereitet für echte Investitionsprozesse.</div>
</div>
</aside>
</div>
<div class="mt-28">
<h2>Marktplatz — Vorschau</h2>
<p class="muted">Eine Auswahl interessanter Pitches. Voller Zugriff im Marktplatz.</p>
<div class="list">
<PitchCard v-for="s in previewStartups" :key="s.id" :pitch="s" />
</div>
</div>
</section>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRuntimeConfig } from '#app';

const previewStartups = ref([]);

onMounted(async () => {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  // Fetch all public pitches from backend
  if (apiBase) {
    try {
      const res = await fetch(`${apiBase}/pitches/`, {
        headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) }
      });
      if (res.ok) {
        const backendPitches = await res.json();
        // Zeige nur die ersten 3 Pitches
        previewStartups.value = backendPitches.slice(0, 3);
        console.debug('Loaded preview pitches from backend:', previewStartups.value.length);
      } else {
        console.warn('Backend pitches request failed with status', res.status);
        // Fallback to demo data
        loadDemoPitches();
      }
    } catch (e) {
      console.warn('Failed to fetch pitches from backend, falling back to demo data', e);
      loadDemoPitches();
    }
  } else {
    loadDemoPitches();
  }
});

function loadDemoPitches() {
  // Fallback: show demo pitches if backend unavailable
  const startups = [
    { id:'s1', title:'SmartHome Energy', sector:'Energy', stage:'Seed', desc:'Dezentrale Energieoptimierung für Privathaushalte mittels Edge-AI und Lastverschiebung.', img:'https://picsum.photos/seed/s1/900/480', goal:'400k€', equity:8 },
    { id:'s2', title:'GreenCharge', sector:'AI', stage:'Series A', desc:'Batterie-Management für EV-Flotten mit optimierter Ladeplanung und Flotten-Analytics.', img:'https://picsum.photos/seed/s2/900/480', goal:'2.5M€', equity:12 },
    { id:'s3', title:'Medico', sector:'Health', stage:'Seed', desc:'Telehealth für chronisch Kranke mit KI-Triage & Adhärenz-Programmen.', img:'https://picsum.photos/seed/s3/900/480', goal:'500k€', equity:6 }
  ];
  previewStartups.value = startups;
}
</script>