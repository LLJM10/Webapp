<template>
  <section id="page-event-detail">
    <!-- Loading State -->
    <div v-if="!event && !error" style="text-align: center; padding: 80px 20px">
      <div style="font-size: 3rem; margin-bottom: 16px">⏳</div>
      <p class="muted">Event wird geladen...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card" style="text-align: center; padding: 48px; margin-top: 48px">
      <h2>Event nicht gefunden</h2>
      <p class="muted" style="margin-top: 16px">
        {{ error }}
      </p>
      <NuxtLink to="/events" class="btn primary" style="margin-top: 24px">
        Zurück zu Events
      </NuxtLink>
    </div>

    <!-- Event Content -->
    <div v-else-if="event">
      <!-- Back Button -->
      <div style="margin-bottom: 24px">
        <NuxtLink to="/events" class="btn ghost" style="display:inline-flex;align-items:center;gap:8px">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/>
          </svg>
          Zurück zu Events
        </NuxtLink>
      </div>

      <!-- Hero Section -->
      <div class="hero-section">
        <img :src="event.img || 'https://picsum.photos/seed/event/1200/400'" :alt="event.name" class="hero-image" />
        <div class="hero-overlay">
          <div class="hero-content">
            <h1 class="hero-title">{{ event.name }}</h1>
            <div class="hero-meta">
              <span class="badge">{{ event.topic }}</span>
              <span class="badge">{{ event.location }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="detail-grid">
        <!-- Left Column: Main Content -->
        <div class="main-content">
          <!-- Description Card -->
          <div class="card description-card">
            <h2 style="margin-bottom: 16px">Über das Event</h2>
            <p style="font-size: 1.125rem; line-height: 1.75; color: var(--muted)">
              {{ event.description }}
            </p>
          </div>

          <!-- Event Details -->
          <div class="card details-card">
            <h2 style="margin-bottom: 24px">Event-Details</h2>
            <div class="details-grid">
              <div class="detail-item">
                <div class="detail-icon">📅</div>
                <div>
                  <div class="detail-label">Datum & Uhrzeit</div>
                  <div class="detail-value">{{ formatEventDate(event.date) }}</div>
                </div>
              </div>
              <div class="detail-item">
                <div class="detail-icon">⏱️</div>
                <div>
                  <div class="detail-label">Dauer</div>
                  <div class="detail-value">{{ event.duration }} Minuten</div>
                </div>
              </div>
              <div class="detail-item">
                <div class="detail-icon">📍</div>
                <div>
                  <div class="detail-label">Location</div>
                  <div class="detail-value">{{ event.location }}</div>
                </div>
              </div>
              <div class="detail-item">
                <div class="detail-icon">👤</div>
                <div>
                  <div class="detail-label">Host</div>
                  <div class="detail-value">{{ event.host }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Topic Section -->
          <div class="card topic-card">
            <h2 style="margin-bottom: 16px">🎯 Thema</h2>
            <p style="font-size: 1.05rem; color: var(--muted)">{{ event.topic }}</p>
          </div>
        </div>

        <!-- Right Column: Sidebar -->
        <aside class="sidebar">
          <!-- CTA Card -->
          <div class="card cta-card">
            <h3 style="margin-bottom: 16px; font-size: 1.25rem">Jetzt teilnehmen!</h3>
            <p class="muted" style="margin-bottom: 20px; font-size: 0.95rem">
              Melde dich für dieses spannende Event an und erweitere dein Netzwerk.
            </p>
            <button v-if="event.link" class="btn primary" style="width: 100%; margin-bottom: 12px" @click="joinEvent">
              <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px">
                <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4Zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2Zm13 2.383-4.708 2.825L15 11.105V5.383Zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741ZM1 11.105l4.708-2.897L1 5.383v5.722Z"/>
              </svg>
              Event beitreten
            </button>
            <button v-else class="btn primary" style="width: 100%; margin-bottom: 12px" @click="requestInfo">
              Info anfordern
            </button>
            <button class="btn ghost" style="width: 100%; margin-bottom: 12px" @click="addToCalendar">
              <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px">
                <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
              </svg>
              Zum Kalender hinzufügen
            </button>
            <button class="btn ghost" style="width: 100%" @click="shareEvent">
              <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px">
                <path d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.499 2.499 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5zm-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/>
              </svg>
              Event teilen
            </button>
          </div>

          <!-- Info Card -->
          <div class="card info-card">
            <h3 style="margin-bottom: 16px; font-size: 1.1rem">Quick Info</h3>
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">Datum</span>
                <span class="info-value">{{ formatShortDate(event.date) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Uhrzeit</span>
                <span class="info-value">{{ formatTime(event.date) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Dauer</span>
                <span class="info-value">{{ event.duration }} Min</span>
              </div>
              <div class="info-item">
                <span class="info-label">Location</span>
                <span class="info-value">{{ event.location }}</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useRuntimeConfig } from '#app';

const route = useRoute();
const event = ref(null);
const error = ref(null);

// Datum-Formatierung
function formatEventDate(dateString) {
  if (!dateString) return 'Datum nicht verfügbar';
  const date = new Date(dateString);
  const weekday = date.toLocaleDateString('de-DE', { weekday: 'long' });
  const day = String(date.getDate()).padStart(2, '0');
  const month = date.toLocaleDateString('de-DE', { month: 'long' });
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${weekday}, ${day}. ${month} ${year} · ${hours}:${minutes} Uhr`;
}

function formatShortDate(dateString) {
  if (!dateString) return '—';
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}.${month}.${year}`;
}

function formatTime(dateString) {
  if (!dateString) return '—';
  const date = new Date(dateString);
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${hours}:${minutes} Uhr`;
}

onMounted(async () => {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const eventId = route.params.id;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  if (!eventId) {
    error.value = 'Event-ID fehlt';
    return;
  }

  // Fallback zu Demo-Daten
  const demoEvents = [
    { id: 1, name: 'MedTech Deep Dive', date: '2025-11-09T14:00', duration: 120, location: 'MS Teams', host: 'HealthInvest', topic: 'Regulierung & Markteintritt', description: 'Panel-Diskussion über Regulierungen im MedTech-Bereich und erfolgreiche Markteintrittstrategien. Experten aus der Branche teilen ihre Erfahrungen und beantworten Fragen.', img: 'https://picsum.photos/seed/e2/900/480', link: 'https://teams.microsoft.com/...' },
    { id: 2, name: 'AI Startup Pitch Night', date: '2025-11-15T18:00', duration: 180, location: 'Berlin HQ', host: 'TechHub', topic: 'AI & ML Startups', description: 'Pitching-Event für AI-fokussierte Startups. 10 ausgewählte Startups präsentieren ihre KI-Lösungen vor Investoren und erhalten wertvolles Feedback.', img: 'https://picsum.photos/seed/e3/900/480', link: '' },
    { id: 3, name: 'SaaS Growth Strategies', date: '2025-11-20T10:00', duration: 90, location: 'Zoom', host: 'GrowthLab', topic: 'SaaS Scaling', description: 'Workshop zu Wachstumsstrategien für SaaS-Unternehmen. Lerne bewährte Methoden für Customer Acquisition, Retention und Skalierung kennen.', img: 'https://picsum.photos/seed/e4/900/480', link: 'https://zoom.us/...' }
  ];

  if (apiBase) {
    try {
      const url = `${apiBase}/events/${eventId}/`;
      const res = await fetch(url, {
        headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) }
      });
      
      if (res.ok) {
        event.value = await res.json();
        return;
      }
    } catch (e) {
      console.warn('Backend nicht erreichbar, lade Demo-Daten');
    }
  }

  // Lade Demo-Event
  const demoEvent = demoEvents.find(e => e.id === parseInt(eventId));
  if (demoEvent) {
    event.value = demoEvent;
  } else {
    error.value = 'Event nicht gefunden';
  }
});

function joinEvent() {
  if (event.value?.link) {
    window.open(event.value.link, '_blank');
  }
}

function requestInfo() {
  alert(`Info für Event "${event.value.name}" wird angefordert.`);
}

function addToCalendar() {
  alert('Kalender-Integration folgt...');
}

function shareEvent() {
  if (navigator.share) {
    navigator.share({
      title: event.value.name,
      text: event.value.description,
      url: window.location.href
    });
  } else {
    navigator.clipboard.writeText(window.location.href);
    alert('Link in Zwischenablage kopiert!');
  }
}
</script>

<style scoped>
/* Hero Section */
.hero-section {
  position: relative;
  width: 100%;
  height: 400px;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 32px;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
  padding: 48px 32px 32px;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  color: white;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.hero-meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.badge {
  background: rgba(94, 234, 212, 0.15);
  color: var(--accent);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  border: 1px solid rgba(94, 234, 212, 0.3);
}

/* Grid Layout */
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 24px;
  margin-top: 24px;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: sticky;
  top: 24px;
  height: fit-content;
}

/* Cards */
.description-card,
.details-card,
.topic-card,
.cta-card,
.info-card {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  padding: 32px;
  border-radius: 12px;
}

/* Details Grid */
.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px;
  background: rgba(94, 234, 212, 0.05);
  border: 1px solid rgba(94, 234, 212, 0.1);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.detail-item:hover {
  background: rgba(94, 234, 212, 0.08);
  border-color: rgba(94, 234, 212, 0.2);
  transform: translateY(-2px);
}

.detail-icon {
  font-size: 2rem;
  line-height: 1;
}

.detail-label {
  color: var(--muted);
  font-size: 0.875rem;
  margin-bottom: 4px;
}

.detail-value {
  color: var(--accent);
  font-size: 1.1rem;
  font-weight: 600;
}

/* Info-Liste */
.info-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-label {
  color: var(--muted);
  font-size: 0.95rem;
}

.info-value {
  color: white;
  font-weight: 600;
  font-size: 1rem;
  text-align: right;
}

/* CTA Card */
.cta-card {
  background: linear-gradient(135deg, rgba(94, 234, 212, 0.1) 0%, rgba(96, 165, 250, 0.1) 100%);
  border: 1px solid rgba(94, 234, 212, 0.2);
}

/* Responsive */
@media (max-width: 1024px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    position: static;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-title {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .hero-section {
    height: 300px;
  }
  
  .hero-overlay {
    padding: 32px 20px 20px;
  }
  
  .hero-title {
    font-size: 1.75rem;
  }
  
  .description-card,
  .details-card,
  .topic-card,
  .cta-card,
  .info-card {
    padding: 24px;
  }
}
</style>
