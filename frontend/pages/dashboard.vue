<template>
  <section id="page-dashboard">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h2>Dashboard</h2>
    </div>

    <!-- START: Nur für Startup-Rolle -->
    <div v-if="user.role === 'startup'">
      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <strong>Meine Pitches</strong>
                <div class="muted" style="margin-top:8px">Management deiner Pitches & Kontakte</div>
            </div>
            <!-- Button zum Öffnen des Modals -->
            <button class="btn primary" @click="openCreateModal">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/></svg>
              Neues Angebot anlegen
            </button>
        </div>
        <div style="margin-top:16px; display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:12px">
            <!-- Bestehende Pitches mit der PitchCard Komponente anzeigen -->
            <PitchCard v-for="pitch in myPitches" :key="pitch.id" :pitch="pitch" :id="`pitch-${pitch.id}`" />
            <div v-if="!myPitches.length" class="card muted" style="text-align:center; padding: 24px;">
              Du hast noch keine Angebote erstellt. Klicke auf "Neues Angebot anlegen", um zu starten!
            </div>
        </div>
      </div>
    </div>
    <!-- ENDE: Nur für Startup-Rolle -->

    <!-- Fallback für andere Rollen wie Investor -->
    <div v-else class="card">
      <strong>Investor Dashboard</strong>
      <div class="muted" style="margin-top:8px">Portfolio-Übersicht & Investment Opportunities</div>
      <div style="margin-top:10px;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px">
        <div class="card"><strong>Portfolio</strong><div class="muted" style="margin-top:6px">Total Investiert: 1.2M€</div></div>
        <div class="card"><strong>Watchlist</strong><div class="muted" style="margin-top:6px">3 Startups</div></div>
      </div>
    </div>

    <!-- Nutzerinfo und Quick Actions bleiben unverändert, aber in einem Grid für besseres Layout -->
     <div style="margin-top:12px;display:grid;grid-template-columns:1fr 360px;gap:12px">
      <div>
         <div class="card">
          <strong>Matching Vorschläge</strong>
           <div style="margin-top:8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px">
             <div v-if="user.role === 'startup'" class="card">
               <strong>Investoren Matches</strong>
               <div class="muted" style="margin-top:8px">Anna Müller · Interesse: Energy</div>
             </div>
             <div v-else class="card">
               <strong>Suggested Deals</strong>
               <div class="muted" style="margin-top:8px">GreenCharge · Match: 87%</div>
             </div>
           </div>
         </div>
      </div>
       <aside>
         <div class="card">
            <h3>Nutzerinfo</h3>
            <div class="input-group"><label>Benutzername</label><div class="muted">{{ user.username }}</div></div>
            <div class="input-group"><label>E-Mail</label><div class="muted">{{ user.email }}</div></div>
            <div class="input-group"><label>Rolle</label><div class="muted">{{ user.role }}</div></div>
        </div>
      </aside>
     </div>

    <!-- Modales Fenster zum Erstellen eines neuen Pitches -->
    <div v-if="showCreateModal" id="create-pitch-modal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="card modal-content">
        <h3>Neues Angebot erstellen</h3>
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
            <!-- Verstecktes Input-Feld, um die `required`-Validierung beizubehalten -->
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
             <label>Geschätzter Firmenwert</label>
             <div class="card" style="font-size: 1.2rem; font-weight: bold; color: var(--accent); padding: 12px;">{{ calculatedValuation }}</div>
          </div>
          
          <div class="input-group">
            <label for="desc">Kurzbeschreibung</label>
            <textarea id="desc" v-model="newPitch.desc" rows="3" placeholder="Beschreibe kurz deine Idee..."></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn ghost" @click="showCreateModal = false">Abbrechen</button>
            <button type="submit" class="btn primary">Angebot erstellen</button>
          </div>
        </form>
      </div>
    </div>

  </section>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue';
// Importiere deine PitchCard Komponente
import PitchCard from '~/components/PitchCard.vue';

const phases = ref(['Pre-Seed', 'Seed', 'Series A', 'Wachstum', 'Reife']);

const user = ref({ username: 'Startup-User', email: 'demo@startup.com', role: 'startup' }); // Default-Werte für Demo
const myPitches = ref([]); // Startet mit einer leeren Liste
const showCreateModal = ref(false);

// Datenmodell für einen neuen Pitch
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

// NEU: Berechnet den Firmenwert automatisch
const calculatedValuation = computed(() => {
  const goal = Number(String(newPitch.value.goal).replace(/[^0-9]/g, ''));
  const equity = newPitch.value.equity;

  if (goal > 0 && equity > 0 && equity <= 100) {
    const valuation = (goal / equity) * 100;
    return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(valuation);
  }
  return null;
});

onMounted(async () => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (token) {
    try {
      const res = await fetch('http://127.0.0.1:8000/users/me/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        user.value.username = data.username || '';
        user.value.email = data.email || '';
        user.value.role = data.profile?.role || data.role || 'startup';
      }
    } catch (e) {
      console.error('Failed fetching /users/me/:', e);
    }
  }

  if (user.value.role === 'startup') {
      myPitches.value = [
        { id: 1, title: 'EcoSolutions', sector: 'Nachhaltigkeit', stage: 'Seed', goal: '250.000€', equity: 15, desc: 'Eine Plattform zur Reduzierung von Plastikmüll in Unternehmen.', img: 'https://placehold.co/600x400/3b82f6/ffffff?text=Eco', valuation: '1.666.667 €' },
      ];
  }
});

async function openCreateModal() {
  showCreateModal.value = true;
  await nextTick();
  const modalElement = document.getElementById('create-pitch-modal');
  if (modalElement) {
    modalElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

function handleCreatePitch() {
  const pitchToAdd = { 
    ...newPitch.value, 
    id: Date.now(),
    valuation: calculatedValuation.value // Fügt den berechneten Wert hinzu
  };

  myPitches.value.unshift(pitchToAdd);
  console.log('Neuer Pitch erstellt:', pitchToAdd);
  showCreateModal.value = false;

  newPitch.value = {
    id: null, title: '', sector: '', stage: '', goal: '', equity: null, desc: '', img: 'https://placehold.co/600x400/22c55e/ffffff?text=Neu'
  };
}
</script>

