<template>
  <div style="margin-top:28px">
  <h2>Marktplatz — Vorschau</h2>
  <p class="muted">Eine Auswahl interessanter Pitches.</p>
  <div class="list">
  <PitchCard v-for="s in previewStartups" :key="s.id" :pitch="s" />
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
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