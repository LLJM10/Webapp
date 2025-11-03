<template>
  <section id="page-dashboard">
    <div class="flex-between">
      <h2>Dashboard</h2>
    </div>

    <!-- START: Nur für Startup-Rolle -->
    <div v-if="user.role === 'startup'">
      <div class="card">
  <div class="flex-between">
            <div>
                <strong>Meine Pitches</strong>
                <div class="muted mt-8">Management deiner Pitches & Kontakte</div>
            </div>
            <!-- Button navigiert jetzt zur eigenen Formular-Seite -->
            <NuxtLink to="/pitches/formular" class="btn primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/></svg>
              Neues Angebot anlegen
            </NuxtLink>
        </div>
  <div class="mt-16 grid-auto-fit-280">
            <!-- Bestehende Pitches mit der PitchCard Komponente anzeigen -->
            <PitchCard v-for="pitch in myPitches" :key="pitch.id" :pitch="pitch" :id="`pitch-${pitch.id}`" />
            <div v-if="!myPitches.length" class="card muted text-center p-24">
              Du hast noch keine Angebote erstellt. Klicke auf "Neues Angebot anlegen", um zu starten!
            </div>
        </div>
      </div>
    </div>
    <!-- ENDE: Nur für Startup-Rolle -->

    <!-- Fallback für andere Rollen wie Investor -->
    <div v-else class="card">
      <strong>Investor Dashboard</strong>
      <div class="muted mt-8">Portfolio-Übersicht & Investment Opportunities</div>
      <div class="mt-10 grid-auto-fit-220">
        <div class="card"><strong>Portfolio</strong><div class="muted mt-6">Total Investiert: 1.2M€</div></div>
        <div class="card"><strong>Watchlist</strong><div class="muted mt-6">3 Startups</div></div>
      </div>
    </div>

    
  <div class="mt-12 grid-1fr-360">
      <div>
         <div class="card">
          <strong>Matching Vorschläge</strong>
           <div class="mt-8 grid-auto-fit-220">
             <div v-if="user.role === 'startup'" class="card">
               <strong>Investoren Matches</strong>
               <div class="muted mt-8">Anna Müller · Interesse: Energy</div>
             </div>
             <div v-else class="card">
               <strong>Suggested Deals</strong>
               <div class="muted mt-8">GreenCharge · Match: 87%</div>
             </div>
           </div>
         </div>

         <!-- NEU: Event Sektion -->
         <div class="card" style="margin-top:12px">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <strong>Meine Events</strong>
                    <div class="muted" style="margin-top:8px">Verwalte deine geplanten Events</div>
                </div>
                <button class="btn primary" @click="openCreateEventModal">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/></svg>
                    Neues Event erstellen
                </button>
            </div>
            <div style="margin-top:16px; display:flex; flex-direction:column; gap:12px;">
                <!-- Liste der existierenden Events -->
                <div v-for="event in myEvents" :key="event.id" class="card">
                     <strong>{{ event.name }}</strong>
                     <div class="muted" style="margin-top: 4px;">{{ event.topic }} · {{ event.location }} · {{ event.duration }} Minuten</div>
                </div>
                <div v-if="!myEvents.length" class="card muted" style="text-align:center; padding: 24px;">
                    Du hast noch keine Events erstellt.
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

    <!-- Pitch-Erstellung wurde in eine eigene Seite verschoben: /pitches/formular -->

    <!-- NEU: Modales Fenster zum Erstellen eines neuen Events -->
    <div v-if="showCreateEventModal" id="create-event-modal" class="modal-overlay" @click.self="showCreateEventModal = false">
      <div class="card modal-content">
        <h3>Neues Event erstellen</h3>
        <p class="muted">Fülle die Felder aus, um ein neues Event zu planen.</p>
        <form @submit.prevent="handleCreateEvent">
          <div class="input-group">
            <label for="eventName">Name des Events</label>
            <input id="eventName" v-model="newEvent.name" type="text" placeholder="z.B. Tech Meetup Berlin" required>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
              <div class="input-group">
                <label for="eventDuration">Dauer in Minuten</label>
                <input id="eventDuration" v-model.number="newEvent.duration" type="number" min="1" placeholder="z.B. 90" required>
              </div>
              <div class="input-group">
                <label for="eventLocation">Ort</label>
                <input id="eventLocation" v-model="newEvent.location" type="text" placeholder="z.B. Berlin oder Online" required>
              </div>
          </div>
          <div class="input-group">
            <label for="eventTopic">Thema</label>
            <input id="eventTopic" v-model="newEvent.topic" type="text" placeholder="z.B. AI & Web3" required>
          </div>
          <div class="input-group">
            <label for="eventLink">Online Link (optional)</label>
            <input id="eventLink" v-model="newEvent.link" type="url" placeholder="https://teams.microsoft.com/...">
          </div>
          <div class="input-group">
            <label for="eventDesc">Beschreibung</label>
            <textarea id="eventDesc" v-model="newEvent.description" rows="3" placeholder="Beschreibe kurz das Event..."></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn ghost" @click="showCreateEventModal = false">Abbrechen</button>
            <button type="submit" class="btn primary">Event erstellen</button>
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
const myEvents = ref([]); // NEU: Liste für Events
const showCreateModal = ref(false);
const showCreateEventModal = ref(false); // NEU: State für Event-Modal

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

// NEU: Datenmodell für ein neues Event
const newEvent = ref({
  id: null,
  name: '',
  duration: null,
  location: '',
  topic: '',
  link: '',
  description: ''
});

// LocalStorage helpers: load/save lists so created items survive page reloads (Option A)
function savePitchesToLocalStorage() {
  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem('myPitches', JSON.stringify(myPitches.value));
    } catch (e) {
      console.warn('Failed to save myPitches to localStorage', e);
    }
  }
}

function saveEventsToLocalStorage() {
  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem('myEvents', JSON.stringify(myEvents.value));
    } catch (e) {
      console.warn('Failed to save myEvents to localStorage', e);
    }
  }
}

// Berechnet den Firmenwert automatisch
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

  // NEW: Load Pitches from backend API first
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/pitches/?mine=true`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const backendPitches = await res.json();
        myPitches.value = backendPitches;
        console.debug('Loaded pitches from backend:', backendPitches.length);
      } else {
        console.warn('Backend pitches request failed with status', res.status);
        // Fallback to localStorage
        loadPitchesFromLocalStorage();
      }
    } catch (e) {
      console.warn('Failed to fetch pitches from backend, falling back to localStorage', e);
      loadPitchesFromLocalStorage();
    }
  } else {
    // No apiBase or no token: fallback to localStorage
    loadPitchesFromLocalStorage();
  }

  // Load saved Events from localStorage if available, otherwise use demo data
  try {
    if (typeof window !== 'undefined') {
      const savedEvents = localStorage.getItem('myEvents');
      if (savedEvents) {
        myEvents.value = JSON.parse(savedEvents);
      } else {
        myEvents.value = [
          { id: 1, name: 'Tech Meetup Berlin', duration: 180, location: 'Berlin', topic: 'AI & Web3', link: 'https://teams.microsoft.com/...', description: 'Ein Networking-Event für Entwickler und Gründer.' }
        ];
      }
    } else {
      myEvents.value = [
        { id: 1, name: 'Tech Meetup Berlin', duration: 180, location: 'Berlin', topic: 'AI & Web3', link: 'https://teams.microsoft.com/...', description: 'Ein Networking-Event für Entwickler und Gründer.' }
      ];
    }
  } catch (e) {
    console.warn('Error loading events from localStorage', e);
  }
});

function loadPitchesFromLocalStorage() {
  try {
    if (typeof window !== 'undefined') {
      const savedPitches = localStorage.getItem('myPitches');
      if (savedPitches) {
        myPitches.value = JSON.parse(savedPitches);
      } else if (user.value.role === 'startup') {
        myPitches.value = [
          { id: 1, title: 'EcoSolutions', sector: 'Nachhaltigkeit', stage: 'Seed', goal: '250.000€', equity: 15, desc: 'Eine Plattform zur Reduzierung von Plastikmüll in Unternehmen.', img: 'https://placehold.co/600x400/3b82f6/ffffff?text=Eco', valuation: '1.666.667 €' },
        ];
      }
    } else {
      // Server-side / non-browser: set demo data
      if (user.value.role === 'startup') {
        myPitches.value = [
          { id: 1, title: 'EcoSolutions', sector: 'Nachhaltigkeit', stage: 'Seed', goal: '250.000€', equity: 15, desc: 'Eine Plattform zur Reduzierung von Plastikmüll in Unternehmen.', img: 'https://placehold.co/600x400/3b82f6/ffffff?text=Eco', valuation: '1.666.667 €' },
        ];
      }
    }
  } catch (e) {
    console.warn('Error loading saved data from localStorage', e);
  }
}

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
  // Persist immediately so the pitch remains after reload
  savePitchesToLocalStorage();
  console.log('Neuer Pitch erstellt:', pitchToAdd);
  showCreateModal.value = false;

  newPitch.value = {
    id: null, title: '', sector: '', stage: '', goal: '', equity: null, desc: '', img: 'https://placehold.co/600x400/22c55e/ffffff?text=Neu'
  };
}

// NEU: Funktion zum Öffnen des Event-Modals
async function openCreateEventModal() {
  showCreateEventModal.value = true;
  await nextTick();
  const modalElement = document.getElementById('create-event-modal');
  if (modalElement) {
    modalElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

// NEU: Funktion zum Erstellen eines Events
function handleCreateEvent() {
  const eventToAdd = { 
    ...newEvent.value, 
    id: Date.now()
  };

  myEvents.value.unshift(eventToAdd);
  // Persist events as well
  saveEventsToLocalStorage();
  console.log('Neues Event erstellt:', eventToAdd);
  showCreateEventModal.value = false;

  newEvent.value = {
    id: null, name: '', duration: null, location: '', topic: '', link: '', description: ''
  };
}
</script>