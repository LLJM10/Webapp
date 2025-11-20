<template>
  <div class="event-card">
    <img :src="event.img || 'https://picsum.photos/seed/event/900/480'" :alt="event.name" class="event-img">
    <div class="event-content">
      <div class="event-header">
        <h3>{{ event.name }}</h3>
        <span class="event-host">Host: {{ event.host }}</span>
      </div>
      <div class="event-meta">
        <span>📅 {{ formatEventDate(event.date) }}</span>
        <span>📍 {{ event.location }}</span>
      </div>
      <p class="event-desc">{{ event.description }}</p>
      <div class="event-actions">
        <button class="btn-event primary" @click="joinEvent">Teilnehmen</button>
        <button class="btn-event ghost" @click="navigateToDetail">Details ansehen</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  event: {
    type: Object,
    required: true
  }
});

const router = useRouter();

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

function navigateToDetail() {
  router.push({ path: '/events/' + props.event.id });
}

function joinEvent() {
  if (props.event.link && props.event.link !== 'https://teams.microsoft.com/...' && props.event.link !== 'https://zoom.us/...') {
    window.open(props.event.link, '_blank');
  } else {
    alert(`Event "${props.event.name}" - Teilnahme-Link folgt.`);
  }
}
</script>

<style scoped>
.event-card {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.event-card:hover {
  transform: translateY(-4px);
  border-color: rgba(94, 234, 212, 0.3);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.event-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.event-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.event-header h3 {
  margin: 0;
  font-size: 1.2rem;
  line-height: 1.3;
}

.event-host {
  font-size: 0.85rem;
  color: var(--muted);
  white-space: nowrap;
}

.event-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 0.9rem;
  color: var(--muted);
}

.event-desc {
  color: var(--muted);
  font-size: 0.95rem;
  line-height: 1.5;
  flex: 1;
}

.event-actions {
  display: flex;
  gap: 10px;
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.btn-event {
  flex: 1;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  text-decoration: none;
  display: inline-block;
}

.btn-event.primary {
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  color: #021;
  border: none;
}

.btn-event.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(94, 234, 212, 0.4);
}

.btn-event.ghost {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
}

.btn-event.ghost:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .event-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
