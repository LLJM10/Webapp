<template>
  <div class="pitch" :class="{ 'pitch-clickable': isOwner }" @click="handleCardClick">
    <div class="meta">
      <div>
        <strong>{{ pitch.title }}</strong>
        <div class="muted">{{ pitch.sector }} · {{ pitch.stage }}</div>
      </div>
      <div class="tags"><div class="tag">{{ pitch.goal }} Ziel</div></div>
    </div>
    <img :src="pitch.img" :alt="pitch.title">
    <div class="muted">{{ pitch.desc }}</div>
    
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
      <NuxtLink :to="`/detail/${pitch.id}`" class="btn ghost" @click.stop>Vorschau</NuxtLink>
      <button class="btn primary" @click.stop="dummyApi('/api/favorite?startup='+pitch.id)">Merken</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '~/stores/auth';
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

// Prüfen, ob der aktuelle User der Owner des Pitches ist
const isOwner = computed(() => {
  return auth.user?.id === props.pitch.owner;
});

// Navigation zur Edit-Seite nur wenn der User der Owner ist
function handleCardClick() {
  if (isOwner.value) {
    router.push({ path: '/pitches/formular', query: { id: props.pitch.id } });
  }
  // Wenn nicht Owner: nichts tun (später Detail-Seite)
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
</style>