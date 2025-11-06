<template>
  <section id="page-detail">
    <div v-if="pitch">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <h2>{{ pitch.title }}</h2>
        <NuxtLink to="/market" class="btn ghost">← Zurück zum Marktplatz</NuxtLink>
      </div>

      <div class="detail-grid">
        <div>
          <div class="card">
            <img :src="pitch.img || 'https://placehold.co/600x400/3b82f6/ffffff?text=Pitch'" :alt="pitch.title" style="width:100%;border-radius:8px;object-fit:cover" />
            <h3 style="margin-top:12px">{{ pitch.sector }} · {{ pitch.stage }}</h3>
            <p class="muted">{{ pitch.desc }}</p>

            <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
              <div class="tag">Ziel: {{ pitch.goal }}</div>
              <div class="tag">Equity: {{ pitch.equity }}%</div>
              <div v-if="pitch.valuation" class="tag">Bewertung: {{ pitch.valuation }}</div>
            </div>

            <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
              <button class="btn primary" @click="dummyApi('/api/favorite?pitch=' + pitch.id)">Merken</button>
              <button class="btn ghost" @click="dummyApi('/api/contact?pitch=' + pitch.id)">Kontakt aufnehmen</button>
            </div>
          </div>
        </div>

        <aside>
          <!-- PDF Dokumente -->
          <div v-if="pitch.pitch_deck || pitch.business_plan || pitch.financial_report" class="card">
            <strong>📎 Dokumente</strong>
            <div style="margin-top:12px;display:flex;flex-direction:column;gap:8px">
              <a v-if="pitch.pitch_deck" 
                 :href="pitch.pitch_deck" 
                 target="_blank" 
                 class="btn ghost" 
                 style="width:100%;text-align:left">
                📄 Pitch Deck herunterladen
              </a>
              <a v-if="pitch.business_plan" 
                 :href="pitch.business_plan" 
                 target="_blank" 
                 class="btn ghost" 
                 style="width:100%;text-align:left">
                📊 Business Plan herunterladen
              </a>
              <a v-if="pitch.financial_report" 
                 :href="pitch.financial_report" 
                 target="_blank" 
                 class="btn ghost" 
                 style="width:100%;text-align:left">
                💰 Financial Report herunterladen
              </a>
            </div>
          </div>
          
          <div class="card" style="margin-top:12px">
            <strong>Details</strong>
            <div class="muted" style="margin-top:8px">Sektor: {{ pitch.sector }}</div>
            <div class="muted">Stage: {{ pitch.stage }}</div>
            <div class="muted">Funding Ziel: {{ pitch.goal }}</div>
            <div class="muted">Equity: {{ pitch.equity }}%</div>
            <div v-if="pitch.valuation" class="muted">Bewertung: {{ pitch.valuation }}</div>
          </div>
        </aside>
      </div>
    </div>
    <div v-else>
      <h2>Pitch nicht gefunden.</h2>
      <p class="muted">Bitte kehren Sie zum <NuxtLink to="/market">Marktplatz</NuxtLink> zurück.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useRuntimeConfig } from '#app';
import { dummyApi } from '~/composables/useDemoData';

const route = useRoute();
const pitch = ref(null);

onMounted(async () => {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const pitchId = route.params.id;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  if (apiBase && pitchId) {
    try {
      const res = await fetch(`${apiBase}/pitches/${pitchId}/`, {
        headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) }
      });
      
      if (res.ok) {
        pitch.value = await res.json();
        console.log('Pitch loaded:', pitch.value);
      } else {
        console.error('Failed to load pitch:', res.status);
      }
    } catch (e) {
      console.error('Error loading pitch:', e);
    }
  }
});
</script>

<style scoped>
.detail-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
  margin-top: 16px;
}

@media (max-width: 768px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>