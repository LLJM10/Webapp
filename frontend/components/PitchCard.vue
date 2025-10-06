<template>
  <div class="pitch" @click="navigateToDetail">
    <div class="meta">
      <div>
        <strong>{{ pitch.title }}</strong>
        <div class="muted">{{ pitch.sector }} · {{ pitch.stage }}</div>
      </div>
      <div class="tags"><div class="tag">{{ pitch.goal }} Ziel</div></div>
    </div>
    <img :src="pitch.img" :alt="pitch.title">
    <div class="muted">{{ pitch.desc }}</div>
    <div style="display:flex;gap:8px;margin-top:8px">
      <NuxtLink :to="`/detail/${pitch.id}`" class="btn ghost" @click.stop>Vorschau</NuxtLink>
      <button class="btn primary" @click.stop="dummyApi('/api/favorite?startup='+pitch.id)">Merken</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
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

// Navigation zur Detailseite, wenn die Karte geklickt wird
function navigateToDetail() {
  // Achtung: Wenn Sie die pages/detail/[id].vue noch nicht korrigiert haben,
  // kann dieser Aufruf fehlschlagen.
  router.push(`/detail/${props.pitch.id}`);
}
</script>