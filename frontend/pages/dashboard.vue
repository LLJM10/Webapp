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
            <!-- Bestehende Pitches mit Edit/Delete Buttons -->
            <div v-for="pitch in myPitches" :key="pitch.id" class="card">
              <!-- Normaler Anzeigemodus -->
              <div v-if="editingPitch?.id !== pitch.id">
                <img :src="pitch.img || 'https://placehold.co/600x400/3b82f6/ffffff?text=Pitch'" :alt="pitch.title" style="width:100%;border-radius:8px;object-fit:cover;height:200px">
                <div style="margin-top:8px">
                  <strong>{{ pitch.title }}</strong>
                  <div class="muted">{{ pitch.sector }} · {{ pitch.stage }}</div>
                </div>
                <p class="muted" style="margin-top:8px">{{ pitch.desc }}</p>
                <div style="display:flex;justify-content:space-between;margin-top:8px">
                  <div class="muted">Ziel: {{ pitch.goal }}</div>
                  <div class="muted">Equity: {{ pitch.equity }}%</div>
                </div>
                <div style="display:flex;gap:8px;margin-top:8px">
                  <button class="btn ghost" @click="startEditPitch(pitch)">Bearbeiten</button>
                  <button class="btn ghost danger" @click="confirmDeletePitch(pitch)">Löschen</button>
                </div>
              </div>

              <!-- Edit-Modus (inline) -->
              <div v-else>
                <div class="input-group">
                  <label>Titel</label>
                  <input v-model="editingPitch.title" type="text">
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
                  <div class="input-group">
                    <label>Sektor</label>
                    <input v-model="editingPitch.sector" type="text">
                  </div>
                  <div class="input-group">
                    <label>Stage</label>
                    <input v-model="editingPitch.stage" type="text">
                  </div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
                  <div class="input-group">
                    <label>Ziel</label>
                    <input v-model="editingPitch.goal" type="text">
                  </div>
                  <div class="input-group">
                    <label>Equity (%)</label>
                    <input v-model.number="editingPitch.equity" type="number">
                  </div>
                </div>
                <div class="input-group">
                  <label>Beschreibung</label>
                  <textarea v-model="editingPitch.desc" rows="3"></textarea>
                </div>
                <div class="input-group">
                  <label>Bild URL</label>
                  <input v-model="editingPitch.img" type="url">
                </div>
                <div style="display:flex;gap:8px;margin-top:8px">
                  <button class="btn primary" @click="savePitchEdit">Speichern</button>
                  <button class="btn ghost" @click="cancelEditPitch">Abbrechen</button>
                </div>
              </div>

              <!-- Delete Confirmation (inline) -->
              <div v-if="pitchToDelete?.id === pitch.id" style="margin-top:8px;padding:12px;background:#fef2f2;border-radius:8px;border:1px solid #fecaca">
                <strong style="color:#dc2626">Wirklich löschen?</strong>
                <p class="muted" style="margin-top:4px">Dieser Pitch wird dauerhaft gelöscht.</p>
                <div style="display:flex;gap:8px;margin-top:8px">
                  <button class="btn danger small" @click="deletePitch">Ja, löschen</button>
                  <button class="btn ghost small" @click="cancelDeletePitch">Abbrechen</button>
                </div>
              </div>
            </div>
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
                  <img :src="event.img || 'https://picsum.photos/seed/event/900/480'" :alt="event.name" style="width:100%;border-radius:8px;object-fit:cover;height:200px">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px">
                    <div>
                      <strong>{{ event.name }}</strong>
                      <div class="muted">{{ formatEventDate(event.date) }} · {{ event.location }}</div>
                    </div>
                    <div class="muted">Host: {{ event.host }}</div>
                  </div>
                  <p class="muted" style="margin-top:8px">{{ event.description }}</p>
                  <div style="display:flex;gap:8px;margin-top:8px">
                    <button class="btn ghost" @click="openEditEventModal(event)">Bearbeiten</button>
                    <button class="btn ghost danger" @click="confirmDeleteEvent(event)">Löschen</button>
                  </div>
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
            <label for="eventName">Name des Events *</label>
            <input 
              id="eventName" 
              v-model="newEvent.name" 
              type="text" 
              placeholder="z.B. Tech Meetup Berlin" 
              :class="{ 'error': validationErrors.name }"
              required
            >
            <span v-if="validationErrors.name" class="error-text">{{ validationErrors.name }}</span>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
              <div class="input-group">
                <label for="eventDuration">Dauer (Minuten) *</label>
                <input 
                  id="eventDuration" 
                  v-model.number="newEvent.duration" 
                  type="number" 
                  min="1" 
                  max="480"
                  placeholder="z.B. 90" 
                  :class="{ 'error': validationErrors.duration }"
                  required
                >
                <span v-if="validationErrors.duration" class="error-text">{{ validationErrors.duration }}</span>
              </div>
              <div class="input-group">
                <label for="eventLocation">Ort/Platform *</label>
                <input 
                  id="eventLocation" 
                  v-model="newEvent.location" 
                  type="text" 
                  placeholder="z.B. MS Teams, Zoom" 
                  :class="{ 'error': validationErrors.location }"
                  required
                >
                <span v-if="validationErrors.location" class="error-text">{{ validationErrors.location }}</span>
              </div>
          </div>
          <div class="input-group">
            <label for="eventTopic">Thema *</label>
            <input 
              id="eventTopic" 
              v-model="newEvent.topic" 
              type="text" 
              placeholder="z.B. AI & Web3" 
              :class="{ 'error': validationErrors.topic }"
              required
            >
            <span v-if="validationErrors.topic" class="error-text">{{ validationErrors.topic }}</span>
          </div>
          <div class="input-group">
            <label for="eventDate">Datum und Uhrzeit *</label>
            <input 
              id="eventDate" 
              v-model="newEvent.date" 
              type="datetime-local" 
              :class="{ 'error': validationErrors.date }"
              required
            >
            <span v-if="validationErrors.date" class="error-text">{{ validationErrors.date }}</span>
          </div>
          <div class="input-group">
            <label for="eventHost">Host/Organisation</label>
            <input 
              id="eventHost" 
              v-model="newEvent.host" 
              type="text" 
              placeholder="z.B. HealthInvest (optional)"
            >
          </div>
          <div class="input-group">
            <label for="eventLink">Online Link (optional)</label>
            <input id="eventLink" v-model="newEvent.link" type="url" placeholder="https://teams.microsoft.com/...">
          </div>
          <div class="input-group">
            <label for="eventImg">Titelbild URL</label>
            <input id="eventImg" v-model="newEvent.img" type="url" placeholder="https://picsum.photos/seed/e1/900/480">
          </div>
          <div class="input-group">
            <label for="eventDesc">Beschreibung *</label>
            <textarea 
              id="eventDesc" 
              v-model="newEvent.description" 
              rows="3" 
              placeholder="Panel: Regulierung & Markteintritt..."
              :class="{ 'error': validationErrors.description }"
              required
            ></textarea>
            <span v-if="validationErrors.description" class="error-text">{{ validationErrors.description }}</span>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn ghost" @click="showCreateEventModal = false">Abbrechen</button>
            <button type="submit" class="btn primary">Event erstellen</button>
          </div>
        </form>
      </div>
    </div>

    <!-- NEU: Edit Event Modal -->
    <div v-if="showEditEventModal" class="modal-overlay" @click.self="showEditEventModal = false">
      <div class="card modal-content">
        <h3>Event bearbeiten</h3>
        <form @submit.prevent="handleUpdateEvent">
          <div class="input-group">
            <label>Name des Events *</label>
            <input v-model="editingEvent.name" type="text" required>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
              <div class="input-group">
                <label>Dauer (Minuten) *</label>
                <input v-model.number="editingEvent.duration" type="number" min="1" max="480" required>
              </div>
              <div class="input-group">
                <label>Ort/Platform *</label>
                <input v-model="editingEvent.location" type="text" required>
              </div>
          </div>
          <div class="input-group">
            <label>Thema *</label>
            <input v-model="editingEvent.topic" type="text" required>
          </div>
          <div class="input-group">
            <label>Datum und Uhrzeit *</label>
            <input v-model="editingEvent.date" type="datetime-local" required>
          </div>
          <div class="input-group">
            <label>Host/Organisation</label>
            <input v-model="editingEvent.host" type="text">
          </div>
          <div class="input-group">
            <label>Online Link</label>
            <input v-model="editingEvent.link" type="url">
          </div>
          <div class="input-group">
            <label>Titelbild URL</label>
            <input v-model="editingEvent.img" type="url">
          </div>
          <div class="input-group">
            <label>Beschreibung *</label>
            <textarea v-model="editingEvent.description" rows="3" required></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn ghost" @click="showEditEventModal = false">Abbrechen</button>
            <button type="submit" class="btn primary">Speichern</button>
          </div>
        </form>
      </div>
    </div>

    <!-- NEU: Delete Confirmation Modal -->
    <div v-if="showDeleteConfirmation" class="modal-overlay" @click.self="showDeleteConfirmation = false">
      <div class="card modal-content">
        <h3>Event löschen?</h3>
        <p class="muted">
          Möchtest du das Event "{{ eventToDelete?.name }}" wirklich löschen? 
          Diese Aktion kann nicht rückgängig gemacht werden.
        </p>
        <div style="display:flex;gap:8px;margin-top:16px;justify-content:flex-end">
          <button class="btn ghost" @click="showDeleteConfirmation = false">Abbrechen</button>
          <button class="btn danger" @click="deleteEvent">Löschen bestätigen</button>
        </div>
      </div>
    </div>

  </section>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue';

const phases = ref(['Pre-Seed', 'Seed', 'Series A', 'Wachstum', 'Reife']);

const user = ref({ username: 'Startup-User', email: 'demo@startup.com', role: 'startup' }); // Default-Werte für Demo
const myPitches = ref([]); // Startet mit einer leeren Liste
const myEvents = ref([]); // NEU: Liste für Events
const showCreateModal = ref(false);
const showCreateEventModal = ref(false); // NEU: State für Event-Modal
const showEditEventModal = ref(false); // State für Edit-Modal
const showDeleteConfirmation = ref(false); // State für Delete-Confirmation
const eventToDelete = ref(null); // Event das gelöscht werden soll
const editingEvent = ref(null); // Event das bearbeitet wird
const validationErrors = ref({}); // Validierungsfehler

// NEU: Pitch Edit/Delete States (inline, keine Modals)
const pitchToDelete = ref(null);
const editingPitch = ref(null);

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
  date: '',
  host: '',
  link: '',
  description: '',
  img: ''
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
  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/events/?mine=true`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const backendEvents = await res.json();
        myEvents.value = backendEvents;
        console.debug('Loaded events from backend:', backendEvents.length);
      } else {
        console.warn('Backend events request failed with status', res.status);
        loadEventsFromLocalStorage();
      }
    } catch (e) {
      console.warn('Failed to fetch events from backend, falling back to localStorage', e);
      loadEventsFromLocalStorage();
    }
  } else {
    loadEventsFromLocalStorage();
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

function loadEventsFromLocalStorage() {
  try {
    if (typeof window !== 'undefined') {
      const savedEvents = localStorage.getItem('myEvents');
      if (savedEvents) {
        myEvents.value = JSON.parse(savedEvents);
      } else {
        myEvents.value = [
          { id: 1, name: 'Tech Meetup Berlin', duration: 180, location: 'MS Teams', topic: 'AI & Web3', date: '2025-11-15T14:00', host: 'TechHub', link: 'https://teams.microsoft.com/...', description: 'Ein Networking-Event für Entwickler und Gründer.', img: 'https://picsum.photos/seed/e1/900/480' }
        ];
      }
    } else {
      myEvents.value = [
        { id: 1, name: 'Tech Meetup Berlin', duration: 180, location: 'MS Teams', topic: 'AI & Web3', date: '2025-11-15T14:00', host: 'TechHub', link: 'https://teams.microsoft.com/...', description: 'Ein Networking-Event für Entwickler und Gründer.', img: 'https://picsum.photos/seed/e1/900/480' }
      ];
    }
  } catch (e) {
    console.warn('Error loading events from localStorage', e);
  }
}

// Datum-Formatierung: "Do, 09.10 · 14:00"
function formatEventDate(dateString) {
  if (!dateString) return 'Datum nicht verfügbar';
  const date = new Date(dateString);
  const weekday = date.toLocaleDateString('de-DE', { weekday: 'short' });
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${weekday}, ${day}.${month} · ${hours}:${minutes}`;
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
  validationErrors.value = {};
  await nextTick();
  const modalElement = document.getElementById('create-event-modal');
  if (modalElement) {
    modalElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

// Validation für Event-Formular
function validateEventForm() {
  validationErrors.value = {};
  let isValid = true;
  
  if (!newEvent.value.name || newEvent.value.name.trim().length < 3) {
    validationErrors.value.name = 'Event-Name muss mindestens 3 Zeichen haben.';
    isValid = false;
  }
  
  if (!newEvent.value.duration || newEvent.value.duration <= 0) {
    validationErrors.value.duration = 'Dauer muss größer als 0 sein.';
    isValid = false;
  } else if (newEvent.value.duration > 480) {
    validationErrors.value.duration = 'Event kann maximal 8 Stunden (480 Min) dauern.';
    isValid = false;
  }
  
  const eventDate = new Date(newEvent.value.date);
  const now = new Date();
  if (!newEvent.value.date) {
    validationErrors.value.date = 'Bitte wähle ein Datum aus.';
    isValid = false;
  } else if (eventDate < now) {
    validationErrors.value.date = 'Event-Datum muss in der Zukunft liegen.';
    isValid = false;
  }
  
  if (!newEvent.value.topic || newEvent.value.topic.trim().length === 0) {
    validationErrors.value.topic = 'Thema ist erforderlich.';
    isValid = false;
  }
  
  if (!newEvent.value.location || newEvent.value.location.trim().length === 0) {
    validationErrors.value.location = 'Ort/Platform ist erforderlich.';
    isValid = false;
  }
  
  if (!newEvent.value.description || newEvent.value.description.trim().length === 0) {
    validationErrors.value.description = 'Beschreibung ist erforderlich.';
    isValid = false;
  }
  
  return isValid;
}

// NEU: Funktion zum Erstellen eines Events (mit Backend)
async function handleCreateEvent() {
  if (!validateEventForm()) {
    return;
  }

  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  const eventData = {
    name: newEvent.value.name,
    topic: newEvent.value.topic,
    location: newEvent.value.location,
    duration: newEvent.value.duration,
    date: newEvent.value.date,
    link: newEvent.value.link || '',
    description: newEvent.value.description,
    img: newEvent.value.img || 'https://picsum.photos/seed/event/900/480',
    host: newEvent.value.host || user.value.username
  };

  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/events/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(eventData)
      });
      
      if (res.ok) {
        const createdEvent = await res.json();
        myEvents.value.unshift(createdEvent);
        console.log('Event erfolgreich erstellt:', createdEvent);
        showCreateEventModal.value = false;
        // Reset form
        newEvent.value = {
          id: null, name: '', duration: null, location: '', topic: '', date: '', host: '', link: '', description: '', img: ''
        };
      } else {
        const errorData = await res.json();
        console.error('Fehler beim Erstellen:', errorData);
        alert('Fehler beim Erstellen: ' + JSON.stringify(errorData));
      }
    } catch (e) {
      console.error('Create event failed:', e);
      alert('Netzwerkfehler beim Erstellen des Events.');
    }
  } else {
    // Fallback: localStorage
    const eventToAdd = { ...eventData, id: Date.now() };
    myEvents.value.unshift(eventToAdd);
    saveEventsToLocalStorage();
    showCreateEventModal.value = false;
    newEvent.value = {
      id: null, name: '', duration: null, location: '', topic: '', date: '', host: '', link: '', description: '', img: ''
    };
  }
}

// Event bearbeiten
function openEditEventModal(event) {
  editingEvent.value = { ...event };
  showEditEventModal.value = true;
}

async function handleUpdateEvent() {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/events/${editingEvent.value.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(editingEvent.value)
      });
      
      if (res.ok) {
        const updated = await res.json();
        const idx = myEvents.value.findIndex(e => e.id === updated.id);
        if (idx !== -1) myEvents.value[idx] = updated;
        console.log('Event erfolgreich aktualisiert');
        showEditEventModal.value = false;
      } else {
        const errorData = await res.json();
        console.error('Fehler beim Aktualisieren:', errorData);
        alert('Fehler: ' + JSON.stringify(errorData));
      }
    } catch (e) {
      console.error('Update failed:', e);
      alert('Netzwerkfehler beim Aktualisieren.');
    }
  }
}

// Event löschen
function confirmDeleteEvent(event) {
  eventToDelete.value = event;
  showDeleteConfirmation.value = true;
}

async function deleteEvent() {
  if (!eventToDelete.value) return;
  
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/events/${eventToDelete.value.id}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (res.ok || res.status === 204) {
        myEvents.value = myEvents.value.filter(e => e.id !== eventToDelete.value.id);
        console.log('Event erfolgreich gelöscht');
        showDeleteConfirmation.value = false;
        eventToDelete.value = null;
      } else {
        console.error('Fehler beim Löschen:', res.status);
        alert('Event konnte nicht gelöscht werden. Bist du der Eigentümer?');
      }
    } catch (e) {
      console.error('Delete failed:', e);
      alert('Netzwerkfehler beim Löschen.');
    }
  }
}

// Pitch bearbeiten (inline)
function startEditPitch(pitch) {
  editingPitch.value = { ...pitch };
}

function cancelEditPitch() {
  editingPitch.value = null;
}

async function savePitchEdit() {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/pitches/${editingPitch.value.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(editingPitch.value)
      });
      
      if (res.ok) {
        const updated = await res.json();
        const idx = myPitches.value.findIndex(p => p.id === updated.id);
        if (idx !== -1) myPitches.value[idx] = updated;
        console.log('Pitch erfolgreich aktualisiert');
        editingPitch.value = null; // Beende Edit-Modus
      } else {
        const errorData = await res.json();
        console.error('Fehler beim Aktualisieren:', errorData);
        alert('Fehler: ' + JSON.stringify(errorData));
      }
    } catch (e) {
      console.error('Update failed:', e);
      alert('Netzwerkfehler beim Aktualisieren.');
    }
  }
}

// Pitch löschen (inline)
function confirmDeletePitch(pitch) {
  // Schließe Edit-Modus falls offen
  if (editingPitch.value?.id === pitch.id) {
    editingPitch.value = null;
  }
  pitchToDelete.value = pitch;
}

function cancelDeletePitch() {
  pitchToDelete.value = null;
}

async function deletePitch() {
  if (!pitchToDelete.value) return;
  
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/pitches/${pitchToDelete.value.id}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (res.ok || res.status === 204) {
        myPitches.value = myPitches.value.filter(p => p.id !== pitchToDelete.value.id);
        console.log('Pitch erfolgreich gelöscht');
        pitchToDelete.value = null;
      } else {
        console.error('Fehler beim Löschen:', res.status);
        alert('Pitch konnte nicht gelöscht werden. Bist du der Eigentümer?');
      }
    } catch (e) {
      console.error('Delete failed:', e);
      alert('Netzwerkfehler beim Löschen.');
    }
  }
}
</script>

<style scoped>
input.error,
textarea.error {
  border-color: #ef4444;
}

.error-text {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 4px;
  display: block;
}

.btn.danger {
  background: #ef4444;
  color: white;
}

.btn.danger:hover {
  background: #dc2626;
}

.btn.small {
  padding: 4px 12px;
  font-size: 0.875rem;
}
</style>