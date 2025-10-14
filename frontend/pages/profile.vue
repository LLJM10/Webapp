<template>
  <section id="page-profile">
    <h2>Profil</h2>
    <div class="card" style="max-width:420px;margin:24px auto 0 auto;">
      <h3>Nutzerinfo</h3>
      <div class="input-group"><label>Benutzername</label><div class="muted">{{ user.username }}</div></div>
      <div class="input-group"><label>E-Mail</label><div class="muted">{{ user.email }}</div></div>
      <div class="input-group"><label>Rolle</label><div class="muted">{{ user.role }}</div></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 320px;gap:12px;margin-top:12px">
      <div>
        <div class="card">
          <div style="display:flex;gap:12px;align-items:center">
            <img :src="profileAvatar" style="width:72px;height:72px;border-radius:10px;object-fit:cover">
            <div>
              <strong>{{ profileName }}</strong>
              <div class="muted">{{ capitalizedRole }}</div>
            </div>
          </div>

          <div style="margin-top:12px">
            <strong>Über mich</strong>
            <p class="muted" style="margin-top:6px">{{ profileBio }}</p>
          </div>
        </div>

        <div style="margin-top:12px" class="card">
          <strong>Dokumente</strong>
          <div class="muted" style="margin-top:8px">CapTable.pdf · PitchDeck.pdf (Demo)</div>
        </div>
      </div>

      <aside>
        <div class="card">
          <strong>Account</strong>
          <div class="muted" style="margin-top:8px">Rolle: <span>{{ capitalizedRole }}</span></div>
          <div style="margin-top:10px">
            <button class="btn ghost" @click="toggleRole">Rolle wechseln</button>
          </div>
        </div>
      </aside>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
const user = ref({ username: '', email: '', role: '' });
onMounted(async () => {
  const token = localStorage.getItem('access_token');
  if (!token) return;
  try {
    const response = await fetch('http://127.0.0.1:8000/users/me/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    user.value.username = data.username;
    user.value.email = data.email;
    user.value.role = data.profile?.role || '';
  } catch (e) {}
});
import { computed } from 'vue';
import { useRole, capitalize } from '~/composables/useDemoData';

const currentRole = useRole();
const capitalizedRole = computed(() => capitalize(currentRole.value));

// Rollen-spezifische Computed Properties
const profileName = computed(() => 
  currentRole.value === 'startup' ? 'Startup Demo' : 'Investor Demo'
);

const profileBio = computed(() => 
  currentRole.value === 'startup' 
    ? 'Gründer / CTO — sucht Seed Funding.' 
    : 'Investor — Fokus: ClimateTech & Health.'
);

const profileAvatar = computed(() => 
  currentRole.value === 'startup' 
    ? 'https://picsum.photos/seed/profileStartup/120/120' 
    : 'https://picsum.photos/seed/profileInvestor/120/120'
);

function toggleRole() {
  currentRole.value = currentRole.value === 'startup' ? 'investor' : 'startup';
}
</script>