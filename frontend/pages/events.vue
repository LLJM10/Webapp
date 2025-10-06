<template>
  <section id="page-events">
    <h2>Events & Sessions</h2>
    <div class="muted">Live-Pitches, Panels und Matchmaking — Demo-Termine.</div>

    <div style="margin-top:14px" class="events-grid">
      <div v-for="ev in events" :key="ev.id" class="card">
        <img :src="ev.img" :alt="ev.title" style="width:100%;border-radius:8px;object-fit:cover">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px">
          <div>
            <strong>{{ ev.title }}</strong>
            <div class="muted">{{ ev.date }} · {{ ev.platform }}</div>
          </div>
          <div class="muted">Hosts: {{ ev.hosts.join(', ') }}</div>
        </div>
        <p class="muted" style="margin-top:8px">{{ ev.desc }}</p>
        <div style="display:flex;gap:8px;margin-top:8px">
          <button class="btn ghost" @click="dummyApi('/api/join?event='+ev.id)">Teilnehmen</button>
          <button class="btn ghost" @click="dummyApi('/api/info?event='+ev.id)">Details</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Die Daten und Logik werden aus dem zentralen Composable importiert
import { events, dummyApi } from '~/composables/useDemoData';

// Optionale Logik: Setzen des Seitentitels (SEO)
useHead({
  title: 'Events & Sessions - investify'
});
</script>

<style scoped>
/* Hier könnten spezifische Stile für diese Seite stehen, wenn nötig */
</style>