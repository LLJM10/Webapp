<template>
  <section id="page-profile" class="profile-page">
    <h2 class="page-title">Profil</h2>

    <div class="profile-grid">
      <div class="left-column">
        <div class="card profile-card">
          <h3>Nutzerinfo</h3>
          <div class="input-group"><label>Benutzername</label><div class="muted">{{ user.username }}</div></div>
          <div class="input-group"><label>E-Mail</label><div class="muted">{{ user.email }}</div></div>
          <div class="input-group"><label>Rolle</label><div class="muted">{{ user.role }}</div></div>
        </div>

        <div class="card profile-overview">
          <div class="profile-header">
            <img :src="profileAvatar" alt="Avatar" class="avatar-img" />
            <div>
              <strong>{{ profileName }}</strong>
              <div class="muted">{{ capitalizedRole }}</div>
            </div>
          </div>

          <div class="profile-about">
            <strong>Über mich</strong>
            <p class="muted">{{ profileBio }}</p>
          </div>
        </div>

        <div class="card docs-card">
          <strong>Dokumente</strong>
          <div class="muted doc-list">CapTable.pdf · PitchDeck.pdf (Demo)</div>
        </div>
      </div>

      <aside class="aside-column">
        <div class="card">
          <strong>Account</strong>
          <div class="muted role-line">Rolle: <span>{{ capitalizedRole }}</span></div>
          <div class="actions">
            <button class="btn" @click="handleLogout">Abmelden</button>
          </div>
        </div>
      </aside>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRole, capitalize } from '~/composables/useDemoData';
import { useAuthStore } from '~/stores/auth';

const user = ref({ username: '', email: '', role: '' });

onMounted(async () => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (!token) return;
  try {
    const response = await fetch('http://127.0.0.1:8000/users/me/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) return;
    const data = await response.json();
    user.value.username = data.username ?? '';
    user.value.email = data.email ?? '';
    user.value.role = data.profile?.role ?? data.role ?? '';
  } catch (err) {
    // ignore network/demo errors
  }
});

const auth = useAuthStore();

function handleLogout() {
  auth.logout();
  if (typeof window !== 'undefined') {
    try {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } catch (e) {}
  }
  navigateTo('/login');
}

const currentRole = useRole();
const capitalizedRole = computed(() => capitalize(currentRole.value));

const profileName = computed(() => (currentRole.value === 'startup' ? 'Startup Demo' : 'Investor Demo'));

const profileBio = computed(() =>
  currentRole.value === 'startup' ? 'Gründer / CTO — sucht Seed Funding.' : 'Investor — Fokus: ClimateTech & Health.'
);

const profileAvatar = computed(() =>
  currentRole.value === 'startup'
    ? 'https://picsum.photos/seed/profileStartup/120/120'
    : 'https://picsum.photos/seed/profileInvestor/120/120'
);
</script>

<style scoped>
/* Mobile-first styles (single-column by default) */
.profile-page { padding: 16px 12px; }
.page-title { margin: 0 0 12px; font-size: 1.5rem; text-align: center; }

.profile-grid { display: block; max-width: 720px; margin: 0 auto; }
.left-column { display: flex; flex-direction: column; gap: 12px; }
.aside-column { margin-top: 12px; }
.profile-card { /* wrapper - inherits .card */ }

/* Profile header */
.profile-header { display:flex; gap:12px; align-items:center; }
.avatar-img { width:56px; height:56px; border-radius:8px; object-fit:cover; }
.profile-about { margin-top:10px; }
.docs-card { margin-top:12px; }
.doc-list { margin-top:8px; }

.role-line { margin-top:8px; }
.actions { margin-top:10px; display:flex; gap:8px; }
.actions .btn { width:100%; }

/* Utilities */
.muted { color: var(--muted); }

/* Desktop and larger screens */
@media (min-width: 800px) {
  .page-title { text-align: left; font-size: 2rem; margin-bottom: 18px; }
  .profile-grid { display: grid; grid-template-columns: 1fr 320px; gap: 20px; margin-top: 12px; max-width:1100px; margin-left:auto; margin-right:auto; align-items:start; }
  .avatar-img { width:72px; height:72px; border-radius:10px; }
  .actions .btn { width: auto; }
}

</style>