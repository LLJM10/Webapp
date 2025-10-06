<template>
  <section id="page-detail">
    <div v-if="startup">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <h2>{{ startup.title }} — Detail</h2>
        <div class="muted">Rolle: <span>{{ capitalizedRole }}</span></div>
      </div>

      <div class="detail-grid">
        <div>
          <div class="card">
            <img :src="startup.img" alt="pitch" style="width:100%;border-radius:8px" />
            <h3 style="margin-top:12px">{{ startup.sector }} · {{ startup.stage }}</h3>
            <p class="muted">{{ startup.desc }}</p>

            <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
              <div v-for="(v, k) in startup.kpis" :key="k" class="tag">{{ k }}: {{ v }}</div>
            </div>

            <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
              <button class="btn primary" @click="performAction">{{ actionLabel }}</button>
              <NuxtLink to="/market" class="btn ghost">Zurück</NuxtLink>
            </div>
          </div>

          <div style="margin-top:12px" class="card">
            <strong>Timeline</strong>
            <div class="muted" style="margin-top:8px">{{ startup.traction }}</div>
          </div>
        </div>

        <aside>
          <div class="card">
            <strong>Dokumente</strong>
            <div class="muted" style="margin-top:8px">CapTable.pdf · PitchDeck.pdf</div>
            <div style="margin-top:10px">
              <button class="btn ghost" @click="dummyApi('/api/northdata?id=demo')">Northdata Lookup</button>
            </div>
          </div>
          <div class="card" style="margin-top:12px">
            <strong>Weitere Kennzahlen</strong>
            <div class="muted" style="margin-top:8px">Valuation: {{ startup.kpis?.valuation || '—' }}</div>
            <div class="muted">Funding Ziel: {{ startup.goal }}</div>
          </div>
        </aside>
      </div>
    </div>
    <div v-else>
      <h2>Startup nicht gefunden.</h2>
      <p class="muted">Bitte kehren Sie zum <NuxtLink to="/market">Marktplatz</NuxtLink> zurück.</p>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';
// Importiere Daten und Logik aus dem Composable
import { startups, useRole, capitalize, dummyApi } from '~/composables/useDemoData';

// Nuxt Hook, um Parameter aus der URL zu lesen (z.B. /detail/s1 -> id='s1')
const route = useRoute();
const pitchId = route.params.id;

// Globaler Rollen-State
const currentRole = useRole();

// Computed Property für das aktuell angezeigte Startup
const startup = computed(() => {
  return startups.find(s => s.id === pitchId);
});

// Computed Properties für das Template
const capitalizedRole = computed(() => capitalize(currentRole.value));

const actionLabel = computed(() => {
  return currentRole.value === 'investor' ? 'Investieren (Demo)' : 'Pitch bearbeiten';
});

// Funktion, die basierend auf der Rolle eine andere Dummy-API aufruft
function performAction() {
  const api = currentRole.value === 'investor' 
    ? `/api/invest?startup=${pitchId}` 
    : `/api/edit?startup=${pitchId}`;
  dummyApi(api);
}

useHead({
  title: computed(() => (startup.value ? startup.value.title : 'Detail') + ' - investify')
});
</script>