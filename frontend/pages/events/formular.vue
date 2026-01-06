<template>
  <section id="page-event-form">
    <AiDescriptionModal 
      :is-open="showAiModal"
      type="event"
      @close="showAiModal = false"
      @generated="handleAiGenerated"
    />
    
    <div class="card" style="max-width:900px;margin:24px auto;">
      <h2>{{ isEditMode ? 'Event bearbeiten' : 'Neues Event erstellen' }}</h2>
      <p class="muted">{{ isEditMode ? 'Bearbeite die Event-Details.' : 'Fülle die Felder aus, um ein neues Event zu erstellen.' }}</p>

      <form @submit.prevent="handleSubmitEvent">
        <div class="input-group">
          <label for="eventName">Name des Events *</label>
          <input 
            id="eventName" 
            v-model="eventForm.name" 
            type="text" 
            placeholder="z.B. Tech Meetup Berlin"
            :class="{ 'error': validationErrors.name }"
            required
          >
          <span v-if="validationErrors.name" class="error-text">{{ validationErrors.name }}</span>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div class="input-group">
            <label for="duration">Dauer (Minuten) *</label>
            <input 
              id="duration" 
              v-model.number="eventForm.duration" 
              type="number" 
              min="1" 
              max="480" 
              placeholder="z.B. 180"
              :class="{ 'error': validationErrors.duration }"
              required
            >
            <span v-if="validationErrors.duration" class="error-text">{{ validationErrors.duration }}</span>
          </div>
          <div class="input-group">
            <label for="location">Ort/Platform *</label>
            <input 
              id="location" 
              v-model="eventForm.location" 
              type="text" 
              placeholder="z.B. MS Teams, Zoom"
              :class="{ 'error': validationErrors.location }"
              required
            >
            <span v-if="validationErrors.location" class="error-text">{{ validationErrors.location }}</span>
          </div>
        </div>

        <div class="input-group">
          <label for="topic">Thema *</label>
          <input 
            id="topic" 
            v-model="eventForm.topic" 
            type="text" 
            placeholder="z.B. AI & Web3"
            :class="{ 'error': validationErrors.topic }"
            required
          >
          <span v-if="validationErrors.topic" class="error-text">{{ validationErrors.topic }}</span>
        </div>

        <div class="input-group">
          <label for="date">Datum und Uhrzeit *</label>
          <input 
            id="date" 
            v-model="eventForm.date" 
            type="datetime-local"
            :class="{ 'error': validationErrors.date }"
            required
          >
          <span v-if="validationErrors.date" class="error-text">{{ validationErrors.date }}</span>
        </div>

        <div class="input-group">
          <label for="host">Host/Organisation</label>
          <input 
            id="host" 
            v-model="eventForm.host" 
            type="text" 
            placeholder="z.B. TechHub"
          >
        </div>

        <div class="input-group">
          <label for="link">Online Link (optional)</label>
          <input 
            id="link" 
            v-model="eventForm.link" 
            type="url" 
            placeholder="https://teams.microsoft.com/..."
          >
        </div>

        <div class="input-group">
          <label for="eventImage">🖼️ Event Bild (JPG/PNG, optional, max. 5MB)</label>
          <input 
            id="eventImage" 
            type="file" 
            accept="image/jpeg,image/png,image/jpg" 
            @change="handleImageChange($event)"
          >
          <small v-if="imageFile" class="muted" style="display:block;margin-top:4px">
            Ausgewählt: {{ imageFile.name }}
          </small>
          <small v-if="existingImage" class="muted" style="display:block;margin-top:4px">
            Aktuell: <a :href="existingImage" target="_blank" style="color:var(--accent)">Vorhandenes Bild anzeigen</a>
          </small>
          <div v-if="imagePreview" style="margin-top: 12px;">
            <img :src="imagePreview" alt="Preview" style="max-width: 300px; max-height: 200px; border-radius: 8px; border: 2px solid var(--accent);">
          </div>
        </div>

        <div class="input-group">
          <label for="description">Beschreibung *</label>
          <div style="position: relative">
            <textarea 
              id="description" 
              v-model="eventForm.description" 
              rows="4" 
              placeholder="Beschreibe das Event..."
              :class="{ 'error': validationErrors.description }"
              required
            ></textarea>
            <button 
              type="button" 
              class="ai-assist-btn" 
              @click="showAiModal = true"
              title="Mit KI verbessern"
            >
              ✨ KI-Assistent
            </button>
          </div>
          <span v-if="validationErrors.description" class="error-text">{{ validationErrors.description }}</span>
        </div>

        <div class="modal-actions" style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
          <NuxtLink to="/dashboard" class="btn ghost">Abbrechen</NuxtLink>
          <button type="submit" class="btn primary">{{ isEditMode ? 'Änderungen speichern' : 'Event erstellen' }}</button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRuntimeConfig } from '#app';
import { useAuthStore } from '~/stores/auth';

const router = useRouter();
const route = useRoute();
const config = useRuntimeConfig();
const auth = useAuthStore();

const showAiModal = ref(false);
const isEditMode = ref(false);
const validationErrors = ref({});

const eventForm = ref({
  id: null,
  name: '',
  duration: null,
  location: '',
  topic: '',
  date: '',
  host: '',
  link: '',
  description: '',
  img: null
});

const imageFile = ref(null);
const imagePreview = ref(null);
const existingImage = ref(null);

function handleImageChange(event) {
  const file = event.target.files[0];
  if (!file) {
    imageFile.value = null;
    imagePreview.value = null;
    return;
  }
  
  // Client-seitige Validierung
  if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
    alert('Bitte nur JPG/PNG Bilder hochladen.');
    event.target.value = '';
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    alert('Bild zu groß. Maximum: 5MB');
    event.target.value = '';
    return;
  }
  
  imageFile.value = file;
  
  // Vorschau erstellen
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
}

// Hilfsfunktion: ISO-Datetime in datetime-local-Format konvertieren
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

onMounted(async () => {
  const id = route.query.id;
  const apiBase = config.public?.apiBase || null;
  const token = auth?.access || (typeof window !== 'undefined' ? localStorage.getItem('access_token') : null);

  if (id) {
    isEditMode.value = true;
    // Event vom Backend laden
    if (apiBase) {
      try {
        const res = await fetch(`${apiBase}/events/${id}/`, { 
          headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) } 
        });
        if (res.ok) {
          const data = await res.json();
          eventForm.value = {
            ...data,
            date: isoToDatetimeLocal(data.date)
          };
          existingImage.value = data.img || null;
          return;
        }
      } catch (e) {
        console.warn('Failed to fetch event from backend', e);
      }
    }

    // Fallback: Versuche von localStorage zu laden
    try {
      const saved = typeof window !== 'undefined' ? localStorage.getItem('myEvents') : null;
      if (saved) {
        const list = JSON.parse(saved);
        const found = list.find(e => String(e.id) === String(id));
        if (found) {
          eventForm.value = {
            ...found,
            date: isoToDatetimeLocal(found.date)
          };
        }
      }
    } catch (e) {
      console.warn('Failed to load event from localStorage', e);
    }
  }
});

function validateEventForm() {
  validationErrors.value = {};
  let isValid = true;
  
  if (!eventForm.value.name || eventForm.value.name.trim().length < 3) {
    validationErrors.value.name = 'Event-Name muss mindestens 3 Zeichen haben.';
    isValid = false;
  }
  
  if (!eventForm.value.duration || eventForm.value.duration <= 0) {
    validationErrors.value.duration = 'Dauer muss größer als 0 sein.';
    isValid = false;
  } else if (eventForm.value.duration > 480) {
    validationErrors.value.duration = 'Event kann maximal 8 Stunden (480 Min) dauern.';
    isValid = false;
  }
  
  const eventDate = new Date(eventForm.value.date);
  const now = new Date();
  if (!eventForm.value.date) {
    validationErrors.value.date = 'Bitte wähle ein Datum aus.';
    isValid = false;
  } else if (eventDate < now) {
    validationErrors.value.date = 'Event-Datum muss in der Zukunft liegen.';
    isValid = false;
  }
  
  if (!eventForm.value.topic || eventForm.value.topic.trim().length === 0) {
    validationErrors.value.topic = 'Thema ist erforderlich.';
    isValid = false;
  }
  
  if (!eventForm.value.location || eventForm.value.location.trim().length === 0) {
    validationErrors.value.location = 'Ort/Platform ist erforderlich.';
    isValid = false;
  }
  
  if (!eventForm.value.description || eventForm.value.description.trim().length === 0) {
    validationErrors.value.description = 'Beschreibung ist erforderlich.';
    isValid = false;
  }
  
  return isValid;
}

async function handleSubmitEvent() {
  if (!validateEventForm()) {
    return;
  }

  const apiBase = config.public?.apiBase || null;
  const token = auth?.access || (typeof window !== 'undefined' ? localStorage.getItem('access_token') : null);

  if (!token) {
    alert('Kein Authentifizierungs-Token gefunden. Bitte neu anmelden.');
    return;
  }

  // FormData für File Upload verwenden
  const formData = new FormData();
  
  formData.append('name', eventForm.value.name);
  formData.append('topic', eventForm.value.topic);
  formData.append('location', eventForm.value.location);
  formData.append('duration', eventForm.value.duration);
  formData.append('date', eventForm.value.date ? new Date(eventForm.value.date).toISOString() : '');
  formData.append('link', eventForm.value.link || '');
  formData.append('description', eventForm.value.description);
  formData.append('host', eventForm.value.host || '');
  formData.append('is_public', 'true');
  
  // Bild hinzufügen (nur wenn ausgewählt)
  if (imageFile.value) {
    formData.append('img', imageFile.value);
  }

  // PATCH (Bearbeiten)
  if (isEditMode.value && apiBase && eventForm.value.id) {
    try {
      let res = await fetch(`${apiBase}/events/${eventForm.value.id}/`, {
        method: 'PATCH',
        headers: {
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: formData
      });
      
      // Token expired? Try refresh
      if (res.status === 401) {
        const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null;
        if (refreshToken) {
          const refreshResponse = await fetch(`${apiBase}/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
          });
          
          if (refreshResponse.ok) {
            const refreshData = await refreshResponse.json();
            const newToken = refreshData.access;
            if (typeof window !== 'undefined') {
              localStorage.setItem('access_token', newToken);
            }
            
            // Retry original request with new token
            res = await fetch(`${apiBase}/events/${eventForm.value.id}/`, {
              method: 'PATCH',
              headers: {
                Authorization: `Bearer ${newToken}`
              },
              body: formData
            });
          }
        }
      }
      
      if (res.ok) { 
        router.push('/dashboard'); 
        return; 
      } else {
        const errorData = await res.text();
        console.error('PATCH error:', res.status, errorData);
        alert('Fehler beim Aktualisieren: ' + res.status);
      }
    } catch (e) { 
      console.error('Failed to PATCH event', e); 
      alert('Netzwerkfehler beim Aktualisieren');
    }
  }

  // POST (Neu erstellen)
  if (!isEditMode.value && apiBase) {
    try {
      let res = await fetch(`${apiBase}/events/`, {
        method: 'POST',
        headers: {
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: formData
      });
      
      // Token expired? Try refresh
      if (res.status === 401) {
        const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null;
        if (refreshToken) {
          const refreshResponse = await fetch(`${apiBase}/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
          });
          
          if (refreshResponse.ok) {
            const refreshData = await refreshResponse.json();
            const newToken = refreshData.access;
            if (typeof window !== 'undefined') {
              localStorage.setItem('access_token', newToken);
            }
            
            // Retry original request with new token
            res = await fetch(`${apiBase}/events/`, {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${newToken}`
              },
              body: formData
            });
          }
        }
      }
      
      if (res.ok) { 
        router.push('/dashboard'); 
        return; 
      } else { 
        const errorData = await res.text();
        console.error('POST error:', res.status, errorData);
        alert('Fehler beim Erstellen: ' + res.status);
      }
    } catch (e) { 
      console.error('Failed to POST event to backend', e); 
      alert('Netzwerkfehler beim Erstellen');
    }
  }

  // Fallback: localStorage (kann keine Files speichern)
  try {
    const eventToAdd = { 
      ...eventForm.value,
      date: eventForm.value.date ? new Date(eventForm.value.date).toISOString() : null,
      is_public: true
    };
    const saved = typeof window !== 'undefined' ? localStorage.getItem('myEvents') : null;
    const list = saved ? JSON.parse(saved) : [];
    if (isEditMode.value && eventForm.value.id) {
      const idx = list.findIndex(e => String(e.id) === String(eventForm.value.id));
      if (idx !== -1) { list[idx] = { ...eventToAdd, id: eventForm.value.id }; }
      else { list.unshift({ ...eventToAdd, id: eventForm.value.id || Date.now() }); }
    } else {
      const withId = { ...eventToAdd, id: Date.now() };
      list.unshift(withId);
    }
    if (typeof window !== 'undefined') localStorage.setItem('myEvents', JSON.stringify(list));
  } catch (e) {
    console.warn('Failed to save event to localStorage', e);
  }

  router.push('/dashboard');
}

function handleAiGenerated(description) {
  eventForm.value.description = description;
}
</script>

<style scoped>
.input-group {
  margin-bottom: 16px;
}

.input-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: var(--text);
}

.input-group input,
.input-group textarea {
  width: 100%;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: white;
  font-family: inherit;
  font-size: 1rem;
  transition: all 0.2s;
}

.input-group input:focus,
.input-group textarea:focus {
  outline: none;
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.08);
}

.input-group input.error,
.input-group textarea.error {
  border-color: #ef4444;
}

.error-text {
  display: block;
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 4px;
}

.ai-assist-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 6px 12px;
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  border: none;
  border-radius: 6px;
  color: #021;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 4px;
}

.ai-assist-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(94, 234, 212, 0.4);
}

.modal-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
