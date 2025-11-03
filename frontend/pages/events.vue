<template>
  <section id="page-events">
    <div style="margin-top:28px">
      <h2>Event Marktplatz — Alle Events</h2>
      <p class="muted">Entdecke interessante Events aus der Community.</p>
      
      <div style="margin-top:20px; display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:16px">
        <div v-for="event in allEvents" :key="event.id" class="card">
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
            <button class="btn ghost" @click="joinEvent(event)">Teilnehmen</button>
            <button class="btn ghost" @click="showEventDetails(event)">Details</button>
          </div>
        </div>
      </div>

      <div v-if="!allEvents.length" class="muted" style="text-align:center;padding:48px;">
        Noch keine Events verfügbar. Erstelle das erste Event auf deinem Dashboard!
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRuntimeConfig } from '#app';

const allEvents = ref([]);

// Datum-Formatierung
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

onMounted(async () => {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  // Fetch all public events from backend
  if (apiBase) {
    try {
      const res = await fetch(`${apiBase}/events/`, {
        headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) }
      });
      if (res.ok) {
        const backendEvents = await res.json();
        allEvents.value = backendEvents;
        console.debug('Loaded all events from backend:', backendEvents.length);
      } else {
        console.warn('Backend events request failed with status', res.status);
        loadDemoEvents();
      }
    } catch (e) {
      console.warn('Failed to fetch events from backend, falling back to demo data', e);
      loadDemoEvents();
    }
  } else {
    loadDemoEvents();
  }
});

function loadDemoEvents() {
  // Fallback: show demo events if backend unavailable
  const events = [
    { id: 'e1', name: 'MedTech Deep Dive', date: '2025-11-09T14:00', location: 'MS Teams', host: 'HealthInvest', topic: 'Regulierung & Markteintritt', description: 'Panel: Regulierung & Markteintritt.', img: 'https://picsum.photos/seed/e2/900/480', link: 'https://teams.microsoft.com/...' },
    { id: 'e2', name: 'AI Startup Pitch Night', date: '2025-11-15T18:00', location: 'Berlin HQ', host: 'TechHub', topic: 'AI & ML Startups', description: 'Pitching-Event für AI-fokussierte Startups.', img: 'https://picsum.photos/seed/e3/900/480', link: '' },
    { id: 'e3', name: 'SaaS Growth Strategies', date: '2025-11-20T10:00', location: 'Zoom', host: 'GrowthLab', topic: 'SaaS Scaling', description: 'Workshop zu Wachstumsstrategien für SaaS-Unternehmen.', img: 'https://picsum.photos/seed/e4/900/480', link: 'https://zoom.us/...' }
  ];
  allEvents.value = events;
}

function joinEvent(event) {
  if (event.link) {
    window.open(event.link, '_blank');
  } else {
    alert(`Event "${event.name}" - Teilnahme-Link folgt.`);
  }
}

function showEventDetails(event) {
  alert(`Event: ${event.name}\nThema: ${event.topic}\nHost: ${event.host}\n\n${event.description}`);
}
</script>

<style scoped>
/* Event-spezifische Styles können hier hinzugefügt werden */
</style>