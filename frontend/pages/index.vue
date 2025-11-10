<template>
<section id="page-landing">
<div class="hero-centered">
  <div class="hero-content">
    <h1 class="large">Investiere in die Innovation von morgen — mit <span style="color:var(--accent)">investify</span>.</h1>
    <p class="lead">Eine sichere B2B-Plattform, die Gründer & verifizierte Investoren zusammenbringt. Pitch hochladen, Investoren finden, Co-Investments organisieren und Wachstum skalieren — alles an einem Ort.</p>
    <div class="cta-row">
      <!-- Dynamischer Button basierend auf Login-Status -->
      <NuxtLink 
        :to="authStore.access ? '/profile' : '/login'" 
        class="btn primary">
        {{ authStore.access ? 'Jetzt Profil bearbeiten' : 'Jetzt einloggen' }}
      </NuxtLink>
      <!-- Marktplatz-Button nur für eingeloggte User -->
      <NuxtLink 
        v-if="authStore.access" 
        to="/market" 
        class="btn ghost">
        Zum Marktplatz
      </NuxtLink>
    </div>
  </div>
</div>

<!-- Features Grid -->
<div class="features-section">
  <div class="grid-3">
    <FeatureCard title="Pitching & Dokumente" desc="Strukturierte Pitch-Profile mit Video, Cap Table und KPIs für bessere Entscheidungen." />
    <FeatureCard title="Verifiziertes Netzwerk" desc="KYC & OpenVerify Workflows, Co-Investor Matching und Due Diligence Tools." />
    <FeatureCard title="Intelligente Matches" desc="AI-gestützte Empfehlungen für Deals, basierend auf Präferenzen & Track Record." />
  </div>
</div>

<!-- KPI Section -->
<div class="kpi-section">
  <div class="kpi-grid">
    <KPICard 
      :value="98" 
      suffix="%" 
      label="Kundenzufriedenheit" 
    />
    <KPICard 
      :value="150" 
      prefix=">" 
      label="Deals abgeschlossen" 
    />
    <KPICard 
      :value="10.5" 
      prefix=">" 
      suffix="M €" 
      label="Transaktionsvolumen" 
    />
    <KPICard 
      :value="100" 
      prefix=">" 
      label="Aktive Investoren" 
    />
  </div>
</div>

<!-- Marktplatz-Vorschau nur für eingeloggte User -->
<div v-if="authStore.access" class="marketplace-preview">
  <h2>Zum Marktplatz</h2>
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
import { useAuthStore } from '~/stores/auth';
import KPICard from '~/components/KPICard.vue';

const authStore = useAuthStore();
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

<style scoped>
#page-landing {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero-centered {
  text-align: center;
  padding: 4rem 0;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-content .large {
  font-size: 3.5rem;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.hero-content .lead {
  font-size: 1.25rem;
  color: var(--muted);
  margin-bottom: 2rem;
  max-width: 720px;
  margin-left: auto;
  margin-right: auto;
}

.cta-row {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 4rem;
}

.features-section {
  margin: 4rem 0;
}

.kpi-section {
  padding: 4rem 0;
  background: linear-gradient(to bottom, transparent, rgba(var(--accent-rgb), 0.03), transparent);
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.marketplace-preview {
  padding: 4rem 0;
  text-align: center;
}

.marketplace-preview h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.marketplace-preview .list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .hero-content .large {
    font-size: 3rem;
  }
}

@media (max-width: 640px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-content .large {
    font-size: 2.5rem;
  }
  
  .cta-row {
    flex-direction: column;
  }
  
  .cta-row .btn {
    width: 100%;
  }
}
</style>