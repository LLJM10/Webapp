<template>
  <div style="margin-top:28px">
  <h2>Marktplatz — Alle Pitches</h2>
  <p class="muted">Eine Auswahl interessanter Pitches aus der Community.</p>
  <div class="list">
  <PitchCard v-for="s in allPitches" :key="s.id" :pitch="s" />
  </div>
  <div v-if="!allPitches.length" class="muted" style="text-align:center;padding:48px;">
    Noch keine Pitches verfügbar. Erstelle den ersten auf deinem Dashboard!
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRuntimeConfig } from '#app';

const allPitches = ref([]);

onMounted(async () => {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  // Alle öffentlichen Pitches vom Backend abrufen
  if (apiBase) {
    try {
      const res = await fetch(`${apiBase}/pitches/`, {
        headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) }
      });
      if (res.ok) {
        const backendPitches = await res.json();
        allPitches.value = backendPitches;
        console.debug('Loaded all pitches from backend:', backendPitches.length);
      } else {
        console.warn('Backend pitches request failed with status', res.status);
        // Fallback auf Demo-Daten
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
  // Fallback: Zeige Demo-Pitches wenn Backend nicht erreichbar
  const startups = [
    { id:'s1', title:'SmartHome Energy', sector:'Energy', stage:'Seed', desc:'Dezentrale Energieoptimierung für Privathaushalte mittels Edge-AI und Lastverschiebung.', img:'https://picsum.photos/seed/s1/900/480', goal:'400k€', equity:8 },
    { id:'s2', title:'GreenCharge', sector:'AI', stage:'Series A', desc:'Batterie-Management für EV-Flotten mit optimierter Ladeplanung und Flotten-Analytics.', img:'https://picsum.photos/seed/s2/900/480', goal:'2.5M€', equity:12 },
    { id:'s3', title:'Medico', sector:'Health', stage:'Seed', desc:'Telehealth für chronisch Kranke mit KI-Triage & Adhärenz-Programmen.', img:'https://picsum.photos/seed/s3/900/480', goal:'500k€', equity:6 }
  ];
  allPitches.value = startups;
}
</script>

<style scoped>
/* Etwas Styling, damit die Seite gut aussieht */
.test-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 40px;
}

h1 {
  color: var(--accent-2); /* Nutzt die Farben aus deiner main.css */
  margin-bottom: 24px;
}
</style>