<template>
  <div class="pitch pitch-clickable" @click="handleCardClick">
    <div class="meta">
      <div>
        <strong>{{ pitch.title }}</strong>
        <div class="muted">{{ pitch.sector }} · {{ pitch.stage }}</div>
      </div>
      <div class="tags"><div class="tag">{{ pitch.goal }}€ Ziel</div></div>
    </div>
    <img :src="getImageUrl(pitch.img)" :alt="pitch.title">
    
    <!-- Investment Details Grid -->
    <div class="investment-details">
      <div class="detail-box">
        <div class="detail-icon">💰</div>
        <div class="detail-content">
          <div class="detail-label">Funding Ziel</div>
          <div class="detail-value">{{ pitch.goal }}€</div>
        </div>
      </div>
      <div class="detail-box">
        <div class="detail-icon">📊</div>
        <div class="detail-content">
          <div class="detail-label">Equity</div>
          <div class="detail-value">{{ pitch.equity }}%</div>
        </div>
      </div>
      <div v-if="pitch.valuation" class="detail-box">
        <div class="detail-icon">💎</div>
        <div class="detail-content">
          <div class="detail-label">Bewertung</div>
          <div class="detail-value">{{ formatValuation(pitch.valuation) }}</div>
        </div>
      </div>
      <div class="detail-box">
        <div class="detail-icon">🚀</div>
        <div class="detail-content">
          <div class="detail-label">Stage</div>
          <div class="detail-value">{{ pitch.stage }}</div>
        </div>
      </div>
    </div>
    
    <!-- PDF Download Links -->
    <div v-if="pitch.pitch_deck || pitch.business_plan || pitch.financial_report" 
         class="card mt-12" 
         style="background:var(--glass);border:1px solid rgba(255,255,255,0.04);padding:12px">
      <div class="muted" style="font-size:0.875rem;margin-bottom:8px;font-weight:600">
        📎 Dokumente
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <a v-if="pitch.pitch_deck" 
           :href="pitch.pitch_deck" 
           target="_blank" 
           class="btn ghost" 
           style="font-size:0.875rem;padding:8px 12px"
           @click.stop>
          📄 Pitch Deck
        </a>
        <a v-if="pitch.business_plan" 
           :href="pitch.business_plan" 
           target="_blank" 
           class="btn ghost" 
           style="font-size:0.875rem;padding:8px 12px"
           @click.stop>
          📊 Business Plan
        </a>
        <a v-if="pitch.financial_report" 
           :href="pitch.financial_report" 
           target="_blank" 
           class="btn ghost" 
           style="font-size:0.875rem;padding:8px 12px"
           @click.stop>
          💰 Financial Report
        </a>
      </div>
    </div>
    
    <div style="display:flex;gap:8px;margin-top:8px">
      <button class="btn ghost" @click.stop="navigateToDetail">Vorschau</button>
      <button class="btn primary" @click.stop="dummyApi('/api/favorite?startup='+pitch.id)">Merken</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '~/stores/auth';
import { useRuntimeConfig } from '#app';
// Wir importieren nur die dummyApi, da die Pitch-Daten über Props kommen
import { dummyApi } from '~/composables/useDemoData'; 

// Props definieren, um Pitch-Daten zu erhalten
const props = defineProps({
  pitch: {
    type: Object,
    required: true
  }
});

// Router-Instanz für die Navigation
const router = useRouter();
const auth = useAuthStore();
const config = useRuntimeConfig();

// Hilfsfunktion zum Abrufen der korrekten Bild-URL
function getImageUrl(imgPath) {
  if (!imgPath) {
    return 'https://placehold.co/600x400/22c55e/ffffff?text=' + encodeURIComponent(props.pitch.title || 'Pitch');
  }
  
  // Wenn es bereits eine vollständige URL ist (http/https), direkt zurückgeben
  if (imgPath.startsWith('http://') || imgPath.startsWith('https://')) {
    return imgPath;
  }
  
  // Wenn es ein relativer Pfad vom Backend ist (z.B. /media/pitch_images/...)
  if (imgPath.startsWith('/media/')) {
    const apiBase = config.public?.apiBase || 'http://127.0.0.1:8000';
    return apiBase + imgPath;
  }
  
  // Wenn es nur ein Dateiname oder relativer Pfad ohne /media/ ist
  const apiBase = config.public?.apiBase || 'http://127.0.0.1:8000';
  return `${apiBase}/media/${imgPath}`;
}

// Prüfen, ob der aktuelle User der Owner des Pitches ist
const isOwner = computed(() => {
  return auth.user?.id === props.pitch.owner;
});

// Navigation zur Edit-Seite nur wenn der User der Owner ist und auf die Card klickt
// Sonst zur Detail-Seite für Nicht-Owner
function handleCardClick() {
  if (isOwner.value) {
    router.push({ path: '/pitches/formular', query: { id: props.pitch.id } });
  } else {
    router.push({ path: '/detail/' + props.pitch.id });
  }
}

// Vorschau-Button führt IMMER zur Detail-Ansicht (auch für Owner)
function navigateToDetail() {
  router.push({ path: '/detail/' + props.pitch.id });
}

function formatValuation(val) {
  if (!val) return '';
  // Entferne € und Leerzeichen, behalte die Zahl
  return val.replace(/\s+/g, ' ');
}
</script>

<style scoped>
.pitch-clickable {
  cursor: pointer;
}

.pitch-clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.investment-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin: 12px 0;
}

.detail-box {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s;
}

.detail-box:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(94, 234, 212, 0.3);
}

.detail-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.detail-content {
  flex: 1;
  min-width: 0;
}

.detail-label {
  font-size: 0.75rem;
  color: var(--muted);
  margin-bottom: 2px;
}

.detail-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--accent);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>