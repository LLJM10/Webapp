<template>
  <section id="page-pitch-form">
    <div class="card" style="max-width:900px;margin:24px auto;">
      <h2>Neues Angebot erstellen</h2>
      <p class="muted">Fülle die Felder aus, um eine neue Pitch Card zu erstellen.</p>

      <form @submit.prevent="handleCreatePitch">
        <div class="input-group">
          <label for="title">Titel des Startups</label>
          <input id="title" v-model="newPitch.title" type="text" placeholder="z.B. GreenCharge" required>
        </div>
        <div class="input-group">
          <label for="sector">Sektor</label>
          <input id="sector" v-model="newPitch.sector" type="text" placeholder="z.B. Energie, SaaS" required>
        </div>
        <div class="input-group">
          <label>Phase</label>
          <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            <button
              v-for="phase in phases"
              :key="phase"
              type="button"
              class="btn"
              :class="{ 'primary': newPitch.stage === phase, 'ghost': newPitch.stage !== phase }"
              @click="newPitch.stage = phase"
            >
              {{ phase }}
            </button>
          </div>
          <input type="hidden" :value="newPitch.stage" required />
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div class="input-group">
            <label for="goal">Finanzierungsziel</label>
            <input id="goal" v-model="newPitch.goal" type="text" placeholder="z.B. 500.000€" required>
          </div>
          <div class="input-group">
            <label for="equity">Anteil in %</label>
            <input id="equity" v-model.number="newPitch.equity" type="number" min="1" max="100" placeholder="z.B. 10" required>
          </div>
        </div>

        <div v-if="calculatedValuation" class="input-group">
           <label>Geschätzter Firmenwert (Pre-Money)</label>
           <div class="card" style="font-size: 1.2rem; font-weight: bold; color: var(--accent); padding: 12px;">{{ calculatedValuation }}</div>
        </div>

        <div class="input-group">
          <label for="desc">Kurzbeschreibung</label>
          <textarea id="desc" v-model="newPitch.desc" rows="3" placeholder="Beschreibe kurz deine Idee..."></textarea>
        </div>

        <div class="modal-actions" style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
          <NuxtLink to="/dashboard" class="btn ghost">Abbrechen</NuxtLink>
          <button type="submit" class="btn primary">Angebot erstellen</button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRuntimeConfig } from '#app';
import { useAuthStore } from '~/stores/auth';

const router = useRouter();
const config = useRuntimeConfig();
const auth = useAuthStore();

const phases = ref(['Pre-Seed', 'Seed', 'Series A', 'Wachstum', 'Reife']);

const newPitch = ref({
  id: null,
  title: '',
  sector: '',
  stage: '',
  goal: '',
  equity: null,
  desc: '',
  img: 'https://placehold.co/600x400/22c55e/ffffff?text=Neu'
});

const calculatedValuation = computed(() => {
  const goal = Number(String(newPitch.value.goal).replace(/[^0-9]/g, ''));
  const equity = newPitch.value.equity;

  if (goal > 0 && equity > 0 && equity <= 100) {
    const valuation = (goal / equity) * 100;
    return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(valuation);
  }
  return null;
});

const route = useRoute();
const isEditMode = ref(false);

onMounted(async () => {
  const id = route.query.id;
  const apiBase = config.public?.apiBase || null;
  const token = auth?.access || (typeof window !== 'undefined' ? localStorage.getItem('access_token') : null);

  if (id) {
    isEditMode.value = true;
    // Try backend GET /pitches/:id/ first
    if (apiBase) {
      try {
        const res = await fetch(`${apiBase}/pitches/${id}/`, { headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) } });
        if (res.ok) {
          const data = await res.json();
          Object.assign(newPitch.value, data);
          return;
        }
      } catch (e) {
        console.warn('Failed to fetch pitch from backend', e);
      }
    }

    // Fallback: try to load from localStorage
    try {
      const saved = typeof window !== 'undefined' ? localStorage.getItem('myPitches') : null;
      if (saved) {
        const list = JSON.parse(saved);
        const found = list.find(p => String(p.id) === String(id));
        if (found) Object.assign(newPitch.value, found);
      }
    } catch (e) {
      console.warn('Failed to load pitch from localStorage', e);
    }
  }
});

async function handleCreatePitch() {
  const pitchToAdd = { 
    ...newPitch.value,
    valuation: calculatedValuation.value
  };

  const apiBase = config.public?.apiBase || null;
  const token = auth?.access || (typeof window !== 'undefined' ? localStorage.getItem('access_token') : null);

  // If editing, PATCH to backend if available
  if (isEditMode.value && apiBase && newPitch.value.id) {
    try {
      const res = await fetch(`${apiBase}/pitches/${newPitch.value.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: JSON.stringify(pitchToAdd)
      });
      if (res.ok) { router.push('/dashboard'); return; }
    } catch (e) { console.warn('Failed to PATCH pitch', e); }
  }

  // Try backend POST if apiBase is configured and not edit-mode
  if (!isEditMode.value && apiBase) {
    try {
      const res = await fetch(`${apiBase}/pitches/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: JSON.stringify(pitchToAdd)
      });
      if (res.ok) { router.push('/dashboard'); return; }
      else { console.warn('Backend returned error when saving pitch', res.status); }
    } catch (e) { console.warn('Failed to POST pitch to backend, falling back to localStorage', e); }
  }

  // Fallback: save locally (localStorage) so the pitch is visible on this device
  try {
    const saved = typeof window !== 'undefined' ? localStorage.getItem('myPitches') : null;
    const list = saved ? JSON.parse(saved) : [];
    if (isEditMode.value && newPitch.value.id) {
      // replace existing
      const idx = list.findIndex(p => String(p.id) === String(newPitch.value.id));
      if (idx !== -1) { list[idx] = { ...pitchToAdd, id: newPitch.value.id }; }
      else { list.unshift({ ...pitchToAdd, id: newPitch.value.id || Date.now() }); }
    } else {
      const withId = { ...pitchToAdd, id: Date.now() };
      list.unshift(withId);
    }
    if (typeof window !== 'undefined') localStorage.setItem('myPitches', JSON.stringify(list));
  } catch (e) {
    console.warn('Failed to save pitch to localStorage', e);
  }

  router.push('/dashboard');
}
</script>
