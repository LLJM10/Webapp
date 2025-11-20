<template>
  <section id="page-dashboard">
    <!-- Dashboard Header -->
    <div class="dashboard-header">
      <div>
        <h2 style="margin-bottom: 8px">Dashboard</h2>
        <p class="muted">Willkommen zurück, {{ user.username }}</p>
      </div>
    </div>

    <!-- START: Nur für Startup-Rolle -->
    <div v-if="user.role === 'startup'" class="dashboard-layout">
      
      <!-- Hauptbereich: 2-Spalten Layout -->
      <div class="dashboard-main">
        
        <!-- Linke Spalte: Pitches -->
        <div class="dashboard-section">
          <div class="section-header">
            <div>
              <h3>Meine Pitches</h3>
              <p class="muted">Verwalte deine Angebote und Kontakte</p>
            </div>
            <NuxtLink to="/pitches/formular" class="btn primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
              </svg>
              Neues Angebot
            </NuxtLink>
          </div>

          <div class="pitches-grid">
            <!-- Bestehende Pitches mit Edit/Delete Buttons -->
            <div v-for="pitch in myPitches" :key="pitch.id" class="pitch-card">
              <img :src="pitch.img || 'https://placehold.co/600x400/3b82f6/ffffff?text=Pitch'" :alt="pitch.title" class="pitch-image">
              <div class="pitch-content">
                <div class="pitch-header">
                  <h4>{{ pitch.title }}</h4>
                  <div class="pitch-meta">
                    <span class="badge-pill">{{ pitch.sector }}</span>
                    <span class="badge-pill">{{ pitch.stage }}</span>
                  </div>
                </div>
                <p class="muted pitch-desc">{{ pitch.desc }}</p>
                
                <div class="pitch-stats">
                  <div class="stat-item">
                    <span class="stat-label">Ziel</span>
                    <span class="stat-value">{{ pitch.goal }}€</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Equity</span>
                    <span class="stat-value">{{ pitch.equity }}%</span>
                  </div>
                </div>
                
                <!-- PDF Dokumente -->
                <div v-if="pitch.pitch_deck || pitch.business_plan || pitch.financial_report" class="pitch-documents">
                  <div class="doc-label">📎 Dokumente</div>
                  <div class="doc-links">
                    <a v-if="pitch.pitch_deck" :href="pitch.pitch_deck" target="_blank" class="doc-link">📄 Deck</a>
                    <a v-if="pitch.business_plan" :href="pitch.business_plan" target="_blank" class="doc-link">📊 Plan</a>
                    <a v-if="pitch.financial_report" :href="pitch.financial_report" target="_blank" class="doc-link">💰 Report</a>
                  </div>
                </div>
                
                <div class="pitch-actions">
                  <NuxtLink :to="`/pitches/formular?id=${pitch.id}`" class="btn-small ghost">Bearbeiten</NuxtLink>
                  <button class="btn-small danger-outline" @click="confirmDeletePitch(pitch)">Löschen</button>
                </div>

                <!-- Delete Confirmation (inline) -->
                <div v-if="pitchToDelete?.id === pitch.id" class="delete-confirmation">
                  <strong style="color:#ef4444">Wirklich löschen?</strong>
                  <p style="margin-top:8px;color:#cbd5e1;font-size:0.9rem">Dieser Pitch wird dauerhaft gelöscht.</p>
                  <div style="display:flex;gap:8px;margin-top:12px">
                    <button class="btn danger small" @click="deletePitch">Ja, löschen</button>
                    <button class="btn ghost small" @click="cancelDeletePitch">Abbrechen</button>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="!myPitches.length" class="empty-state">
              <div class="empty-icon">📊</div>
              <p class="empty-text">Noch keine Angebote erstellt</p>
              <NuxtLink to="/pitches/formular" class="btn primary empty-cta">
                Erstes Angebot anlegen
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Rechte Spalte: Events -->
        <div class="dashboard-section">
          <div class="section-header">
            <div>
              <h3>Meine Events</h3>
              <p class="muted">Verwalte deine geplanten Events</p>
            </div>
            <button class="btn primary" @click="openCreateEventModal">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
              </svg>
              Neues Event
            </button>
          </div>

          <div class="events-list">
            <div v-for="event in myEvents" :key="event.id" class="event-card">
              <img :src="event.img || 'https://picsum.photos/seed/event/900/480'" :alt="event.name" class="event-image">
              <div class="event-content">
                <h4>{{ event.name }}</h4>
                <div class="event-meta">
                  <span>📅 {{ formatEventDate(event.date) }}</span>
                  <span>📍 {{ event.location }}</span>
                </div>
                <p class="muted event-desc">{{ event.description }}</p>
                <div class="event-actions">
                  <button class="btn-small ghost" @click="openEditEventModal(event)">Bearbeiten</button>
                  <button class="btn-small danger-outline" @click="confirmDeleteEvent(event)">Löschen</button>
                </div>
              </div>
            </div>
            
            <div v-if="!myEvents.length" class="empty-state">
              <div class="empty-icon">📅</div>
              <p class="empty-text">Noch keine Events erstellt</p>
              <button class="btn primary empty-cta" @click="openCreateEventModal">
                Erstes Event erstellen
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar: Nutzerinfo & Matching -->
      <aside class="dashboard-sidebar">
        <div class="sidebar-card">
          <h3>Nutzerinfo</h3>
          <div class="user-info">
            <div class="info-row">
              <span class="info-label">Benutzername</span>
              <span class="info-value">{{ user.username }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">E-Mail</span>
              <span class="info-value">{{ user.email }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Rolle</span>
              <span class="info-value">{{ user.role }}</span>
            </div>
          </div>
        </div>

        <div class="sidebar-card">
          <h3>Matching Vorschläge</h3>
          <div class="match-item">
            <div class="match-avatar">AM</div>
            <div>
              <div class="match-name">Anna Müller</div>
              <div class="muted" style="font-size: 0.875rem">Interesse: Energy</div>
            </div>
          </div>
        </div>
      </aside>

    </div>
    <!-- ENDE: Nur für Startup-Rolle -->

    <!-- Fallback für andere Rollen wie Investor -->
    <div v-else class="dashboard-layout">
      <div class="dashboard-main">
        <div class="dashboard-section">
          <div class="section-header">
            <h3>Investor Dashboard</h3>
            <p class="muted">Portfolio-Übersicht & Investment Opportunities</p>
          </div>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">💼</div>
              <div>
                <div class="stat-label">Portfolio</div>
                <div class="stat-value">1.2M€</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">⭐</div>
              <div>
                <div class="stat-label">Watchlist</div>
                <div class="stat-value">3 Startups</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <aside class="dashboard-sidebar">
        <div class="sidebar-card">
          <h3>Matching Vorschläge</h3>
          <div class="match-item">
            <div class="match-avatar">GC</div>
            <div>
              <div class="match-name">GreenCharge</div>
              <div class="muted" style="font-size: 0.875rem">Match: 87%</div>
            </div>
          </div>
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

// NEU: Pitch Delete State
const pitchToDelete = ref(null);

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

// Helper: convert an ISO datetime (possibly with timezone) to a string
// accepted by <input type="datetime-local"> ("YYYY-MM-DDTHH:MM").
function isoToDatetimeLocal(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (isNaN(d.getTime())) return '';
  const pad = (n) => String(n).padStart(2, '0');
  const yyyy = d.getFullYear();
  const MM = pad(d.getMonth() + 1);
  const dd = pad(d.getDate());
  const hh = pad(d.getHours());
  const mm = pad(d.getMinutes());
  return `${yyyy}-${MM}-${dd}T${hh}:${mm}`;
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
    // convert local datetime-local value to ISO before sending to backend
    date: newEvent.value.date ? new Date(newEvent.value.date).toISOString() : null,
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
  // copy event and normalize date for datetime-local input
  editingEvent.value = { ...event, date: isoToDatetimeLocal(event.date) };
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
        // ensure date is sent as ISO string (backend expects timezone-aware datetime)
        body: JSON.stringify({
          ...editingEvent.value,
          date: editingEvent.value.date ? new Date(editingEvent.value.date).toISOString() : null
        })
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

// Pitch löschen
function confirmDeletePitch(pitch) {
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
/* Dashboard Layout */
.dashboard-header {
  margin-bottom: 32px;
}

.dashboard-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 24px;
  align-items: start;
}

.dashboard-main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.dashboard-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.section-header h3 {
  font-size: 1.25rem;
  margin-bottom: 4px;
}

.section-header p {
  font-size: 0.9rem;
}

/* Pitches Grid */
.pitches-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.pitch-card {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.pitch-card:hover {
  border-color: rgba(94, 234, 212, 0.2);
  transform: translateY(-2px);
}

.pitch-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.pitch-content {
  padding: 16px;
}

.pitch-header {
  margin-bottom: 12px;
}

.pitch-header h4 {
  font-size: 1.1rem;
  margin: 0 0 8px 0;
}

.pitch-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.badge-pill {
  padding: 4px 12px;
  background: rgba(94, 234, 212, 0.1);
  border: 1px solid rgba(94, 234, 212, 0.2);
  border-radius: 20px;
  font-size: 0.8rem;
  color: var(--accent);
  font-weight: 600;
}

.pitch-desc {
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 12px;
}

.pitch-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.stat-item {
  padding: 10px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--muted);
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--accent);
}

.pitch-documents {
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
  margin-bottom: 12px;
}

.doc-label {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--muted);
}

.doc-links {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.doc-link {
  padding: 6px 12px;
  background: rgba(94, 234, 212, 0.05);
  border: 1px solid rgba(94, 234, 212, 0.1);
  border-radius: 6px;
  font-size: 0.85rem;
  text-decoration: none;
  color: var(--accent);
  transition: all 0.2s ease;
}

.doc-link:hover {
  background: rgba(94, 234, 212, 0.1);
  border-color: rgba(94, 234, 212, 0.3);
}

.pitch-actions {
  display: flex;
  gap: 8px;
}

/* Events List */
.events-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.event-card {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.event-card:hover {
  border-color: rgba(96, 165, 250, 0.2);
  transform: translateY(-2px);
}

.event-image {
  width: 100%;
  height: 140px;
  object-fit: cover;
}

.event-content {
  padding: 16px;
}

.event-content h4 {
  font-size: 1.05rem;
  margin: 0 0 8px 0;
}

.event-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
  font-size: 0.875rem;
  color: var(--muted);
}

.event-desc {
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 12px;
}

.event-actions {
  display: flex;
  gap: 8px;
}

/* Sidebar */
.dashboard-sidebar {
  position: sticky;
  top: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-card {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  padding: 20px;
}

.sidebar-card h3 {
  font-size: 1.1rem;
  margin: 0 0 16px 0;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.info-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-label {
  font-size: 0.9rem;
  color: var(--muted);
}

.info-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: white;
}

.match-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.match-item:hover {
  background: rgba(255, 255, 255, 0.04);
}

.match-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #021;
}

.match-name {
  font-weight: 600;
  margin-bottom: 4px;
}

/* Stats Grid (für Investor) */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: rgba(94, 234, 212, 0.2);
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 2rem;
}

/* Button Styles */
.btn-small {
  padding: 8px 14px;
  border-radius: 8px;
  border: 0;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-small.ghost {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
}

.btn-small.ghost:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}

.btn-small.danger-outline {
  background: transparent;
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.btn-small.danger-outline:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.5);
}

/* Empty State */
.empty-state {
  padding: 48px 24px;
  text-align: center;
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-icon {
  font-size: 3.5rem;
  opacity: 0.5;
}

.empty-text {
  color: var(--muted);
  margin: 0;
  font-size: 1rem;
}

.empty-cta {
  margin-top: 8px;
}

/* Responsive */
@media (max-width: 1200px) {
  .dashboard-layout {
    grid-template-columns: 1fr;
  }
  
  .dashboard-sidebar {
    position: static;
  }
}

@media (max-width: 968px) {
  .dashboard-main {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .section-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .pitch-stats {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

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

/* Delete Confirmation Styling */
.delete-confirmation {
  margin-top: 12px;
  padding: 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  backdrop-filter: blur(8px);
}
</style>