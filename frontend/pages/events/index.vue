<template>
  <section id="page-events">
    <div class="events-header">
      <div>
        <h2>Event Marktplatz</h2>
        <p class="muted">Entdecke interessante Events aus der Community</p>
      </div>
    </div>

    <div class="events-grid">
      <EventCard v-for="event in allEvents" :key="event.id" :event="event" />
    </div>

    <div v-if="!allEvents.length" class="empty-events">
      <div class="empty-icon">📅</div>
      <p>Noch keine Events verfügbar</p>
      <p class="muted" style="margin-top: 8px">Erstelle das erste Event auf deinem Dashboard!</p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRuntimeConfig } from '#app';

const allEvents = ref([]);

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
      } else {
        console.warn('Backend events request failed with status', res.status);
        loadDemoEvents();
      }
    } catch (e) {
      console.warn('Failed to fetch events from backend:', e);
      loadDemoEvents();
    }
  } else {
    loadDemoEvents();
  }
});

function loadDemoEvents() {
  const events = [
    { id: 1, name: 'MedTech Deep Dive', date: '2025-11-09T14:00', duration: 120, location: 'MS Teams', host: 'HealthInvest', topic: 'Regulierung & Markteintritt', description: 'Panel: Regulierung & Markteintritt.', img: 'https://picsum.photos/seed/e2/900/480', link: 'https://teams.microsoft.com/...' },
    { id: 2, name: 'AI Startup Pitch Night', date: '2025-11-15T18:00', duration: 180, location: 'Berlin HQ', host: 'TechHub', topic: 'AI & ML Startups', description: 'Pitching-Event für AI-fokussierte Startups.', img: 'https://picsum.photos/seed/e3/900/480', link: '' },
    { id: 3, name: 'SaaS Growth Strategies', date: '2025-11-20T10:00', duration: 90, location: 'Zoom', host: 'GrowthLab', topic: 'SaaS Scaling', description: 'Workshop zu Wachstumsstrategien für SaaS-Unternehmen.', img: 'https://picsum.photos/seed/e4/900/480', link: 'https://zoom.us/...' }
  ];
  allEvents.value = events;
}
</script>

<style scoped>
.events-header {
  margin-bottom: 32px;
}

.events-header h2 {
  margin-bottom: 8px;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.empty-events {
  text-align: center;
  padding: 80px 24px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  opacity: 0.4;
}

@media (max-width: 768px) {
  .events-grid {
    grid-template-columns: 1fr;
  }
}
</style>