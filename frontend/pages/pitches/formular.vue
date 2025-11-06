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

        <!-- PDF Upload Felder -->
        <div class="input-group">
          <label for="pitch_deck">📄 Pitch Deck (PDF, optional, max. 10MB)</label>
          <input 
            id="pitch_deck" 
            type="file" 
            accept=".pdf" 
            @change="handleFileChange($event, 'pitch_deck')"
          >
          <small v-if="pdfFiles.pitch_deck" class="muted" style="display:block;margin-top:4px">
            Ausgewählt: {{ pdfFiles.pitch_deck.name }}
          </small>
          <small v-if="existingFiles.pitch_deck" class="muted" style="display:block;margin-top:4px">
            Aktuell: <a :href="existingFiles.pitch_deck" target="_blank" style="color:var(--accent)">Vorhandenes PDF anzeigen</a>
          </small>
        </div>

        <div class="input-group">
          <label for="business_plan">📊 Business Plan (PDF, optional, max. 10MB)</label>
          <input 
            id="business_plan" 
            type="file" 
            accept=".pdf" 
            @change="handleFileChange($event, 'business_plan')"
          >
          <small v-if="pdfFiles.business_plan" class="muted" style="display:block;margin-top:4px">
            Ausgewählt: {{ pdfFiles.business_plan.name }}
          </small>
          <small v-if="existingFiles.business_plan" class="muted" style="display:block;margin-top:4px">
            Aktuell: <a :href="existingFiles.business_plan" target="_blank" style="color:var(--accent)">Vorhandenes PDF anzeigen</a>
          </small>
        </div>

        <div class="input-group">
          <label for="financial_report">💰 Financial Report (PDF, optional, max. 10MB)</label>
          <input 
            id="financial_report" 
            type="file" 
            accept=".pdf" 
            @change="handleFileChange($event, 'financial_report')"
          >
          <small v-if="pdfFiles.financial_report" class="muted" style="display:block;margin-top:4px">
            Ausgewählt: {{ pdfFiles.financial_report.name }}
          </small>
          <small v-if="existingFiles.financial_report" class="muted" style="display:block;margin-top:4px">
            Aktuell: <a :href="existingFiles.financial_report" target="_blank" style="color:var(--accent)">Vorhandenes PDF anzeigen</a>
          </small>
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

const pdfFiles = ref({
  pitch_deck: null,
  business_plan: null,
  financial_report: null
});

const existingFiles = ref({
  pitch_deck: null,
  business_plan: null,
  financial_report: null
});

function handleFileChange(event, fieldName) {
  const file = event.target.files[0];
  if (!file) {
    pdfFiles.value[fieldName] = null;
    return;
  }
  
  // Client-seitige Validierung
  if (file.type !== 'application/pdf') {
    alert('Bitte nur PDF-Dateien hochladen.');
    event.target.value = '';
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    alert('Datei zu groß. Maximum: 10MB');
    event.target.value = '';
    return;
  }
  
  pdfFiles.value[fieldName] = file;
}

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
          
          // Existierende PDFs laden
          existingFiles.value.pitch_deck = data.pitch_deck || null;
          existingFiles.value.business_plan = data.business_plan || null;
          existingFiles.value.financial_report = data.financial_report || null;
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
  const apiBase = config.public?.apiBase || null;
  const token = auth?.access || (typeof window !== 'undefined' ? localStorage.getItem('access_token') : null);

  if (!token) {
    alert('Kein Authentifizierungs-Token gefunden. Bitte neu anmelden.');
    return;
  }

  // FormData für File Upload verwenden
  const formData = new FormData();
  
  // Text-Felder hinzufügen
  formData.append('title', newPitch.value.title);
  formData.append('sector', newPitch.value.sector);
  formData.append('stage', newPitch.value.stage);
  formData.append('goal', newPitch.value.goal);
  formData.append('equity', newPitch.value.equity);
  formData.append('desc', newPitch.value.desc || '');
  formData.append('img', newPitch.value.img || '');
  formData.append('valuation', calculatedValuation.value || '');
  formData.append('is_public', 'true');
  
  // PDF-Dateien hinzufügen (nur wenn ausgewählt)
  if (pdfFiles.value.pitch_deck) {
    formData.append('pitch_deck', pdfFiles.value.pitch_deck);
  }
  if (pdfFiles.value.business_plan) {
    formData.append('business_plan', pdfFiles.value.business_plan);
  }
  if (pdfFiles.value.financial_report) {
    formData.append('financial_report', pdfFiles.value.financial_report);
  }

  // PATCH (Bearbeiten)
  if (isEditMode.value && apiBase && newPitch.value.id) {
    try {
      const res = await fetch(`${apiBase}/pitches/${newPitch.value.id}/`, {
        method: 'PATCH',
        headers: {
          ...(token ? { Authorization: `Bearer ${token}` } : {})
          // WICHTIG: KEIN Content-Type Header - Browser setzt automatisch mit boundary
        },
        body: formData
      });
      if (res.ok) { 
        router.push('/dashboard'); 
        return; 
      } else {
        const errorData = await res.text();
        console.error('PATCH error:', res.status, errorData);
        alert('Fehler beim Aktualisieren: ' + res.status);
      }
    } catch (e) { 
      console.error('Failed to PATCH pitch', e); 
      alert('Netzwerkfehler beim Aktualisieren');
    }
  }

  // POST (Neu erstellen)
  if (!isEditMode.value && apiBase) {
    try {
      const res = await fetch(`${apiBase}/pitches/`, {
        method: 'POST',
        headers: {
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: formData
      });
      
      if (res.ok) { 
        const createdPitch = await res.json();
        router.push('/dashboard'); 
        return; 
      } else { 
        const errorData = await res.text();
        console.error('POST error:', res.status, errorData);
        alert('Fehler beim Erstellen: ' + res.status);
      }
    } catch (e) { 
      console.error('Failed to POST pitch to backend', e); 
      alert('Netzwerkfehler beim Erstellen');
    }
  }

  // Fallback: localStorage (kann keine Files speichern)
  try {
    const pitchToAdd = { 
      ...newPitch.value,
      valuation: calculatedValuation.value,
      is_public: true
    };
    const saved = typeof window !== 'undefined' ? localStorage.getItem('myPitches') : null;
    const list = saved ? JSON.parse(saved) : [];
    if (isEditMode.value && newPitch.value.id) {
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
