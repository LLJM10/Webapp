<template>
  <section id="page-dashboard">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h2>Dashboard</h2>
      <div class="muted">Rolle: <strong>{{ capitalizedRole }}</strong></div>
    </div>
    <div class="card" style="max-width:420px;margin:24px auto 0 auto;">
      <h3>Nutzerinfo</h3>
      <div class="input-group"><label>Benutzername</label><div class="muted">{{ user.username }}</div></div>
      <div class="input-group"><label>E-Mail</label><div class="muted">{{ user.email }}</div></div>
      <div class="input-group"><label>Rolle</label><div class="muted">{{ user.role }}</div></div>
    </div>

    <div style="margin-top:12px;display:grid;grid-template-columns:1fr 360px;gap:12px">
      <div>
        <div class="card">
          <div v-if="currentRole === 'startup'">
            <strong>Startup Dashboard</strong>
            <div class="muted" style="margin-top:8px">Management deiner Pitches & Kontakte</div>
            <div style="margin-top:10px;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px">
              <div v-for="s in myPitches" :key="s.id" class="card">
                <strong>{{ s.title }}</strong>
                <div class="muted" style="margin-top:6px">{{ s.stage }} · {{ s.sector }}</div>
                <div style="margin-top:8px;display:flex;gap:8px">
                  <NuxtLink :to="`/detail/${s.id}`" class="btn ghost">Bearbeiten</NuxtLink>
                  <button class="btn primary" @click="dummyApi('/api/share?startup='+s.id)">Teilen</button>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <strong>Investor Dashboard</strong>
            <div class="muted" style="margin-top:8px">Portfolio-Übersicht & Investment Opportunities</div>
            <div style="margin-top:10px;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px">
              <div class="card"><strong>Portfolio</strong><div class="muted" style="margin-top:6px">Total Investiert: 1.2M€</div></div>
              <div class="card"><strong>Watchlist</strong><div class="muted" style="margin-top:6px">3 Startups</div></div>
            </div>
          </div>
        </div>

        <div style="margin-top:12px" class="card">
          <strong>Matching Vorschläge</strong>
          <div style="margin-top:8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px">
            <div v-if="currentRole === 'startup'" class="card">
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
          <strong>Quick Actions</strong>
          <div style="margin-top:10px;display:flex;flex-direction:column;gap:8px">
            <NuxtLink to="/market" class="btn ghost">Marktplatz</NuxtLink>
            <NuxtLink to="/events" class="btn ghost">Events</NuxtLink>
            <NuxtLink to="/network" class="btn ghost">Networking</NuxtLink>
          </div>
        </div>

        <div class="card" style="margin-top:12px">
          <strong>Notizen</strong>
          <div class="muted" style="margin-top:8px">Persönliche To-Dos & Erinnerungen (Demo)</div>
        </div>
      </aside>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
const user = ref({ username: '', email: '', role: '' });
onMounted(() => {
  user.value.username = localStorage.getItem('user_username') || '';
  user.value.email = localStorage.getItem('user_email') || '';
  user.value.role = localStorage.getItem('user_role') || '';
});



const currentRole = typeof useRole === 'function' ? useRole() : { value: 'startup' };
const capitalizedRole = computed(() => capitalize(currentRole.value));
const myPitches = Array.isArray(startups) ? startups.slice(0, 2) : [];
</script>