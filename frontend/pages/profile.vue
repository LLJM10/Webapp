<template>
  <section id="page-profile" class="profile-page">
    <!-- Header -->
    <div class="profile-header">
      <div class="header-content">
        <h1 class="page-title">Mein Profil</h1>
        <div class="role-badge" :class="user.role">
          {{ user.role === 'startup' ? 'Startup' : 'Investor' }}
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="successMessage" class="alert alert-success">
      <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
        <polyline points="22 4 12 14.01 9 11.01"/>
      </svg>
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="alert alert-error">
      <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="15" y1="9" x2="9" y2="15"/>
        <line x1="9" y1="9" x2="15" y2="15"/>
      </svg>
      {{ errorMessage }}
    </div>

    <!-- Profile Content -->
    <div class="profile-content">
      <!-- Profile Card -->
      <div class="card-base profile-card">
        <div class="profile-avatar-section">
          <div class="avatar-wrapper">
            <img :src="avatarUrl" :alt="user.username" class="avatar" />
            <div class="avatar-badge" :class="user.role">
              {{ user.role === 'startup' ? '🚀' : '💼' }}
            </div>
          </div>
          <div class="profile-info">
            <h2 class="profile-name">{{ user.username }}</h2>
            <p class="profile-role">{{ user.role === 'startup' ? 'Startup Gründer' : 'Investor' }}</p>
          </div>
        </div>

        <!-- Account Details -->
        <div class="info-section">
          <h3 class="section-heading">Account Details</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Benutzername</span>
              <span class="info-value">{{ user.username }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Rolle</span>
              <span class="info-value">{{ user.role === 'startup' ? 'Startup' : 'Investor' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Mitglied seit</span>
              <span class="info-value">{{ formattedJoinDate }}</span>
            </div>
          </div>
        </div>

        <!-- Email Edit Section -->
        <div class="info-section">
          <div class="section-header">
            <h3 class="section-heading">E-Mail Adresse</h3>
            <button v-if="!isEditingEmail" @click="startEditEmail" class="btn-edit">
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              Bearbeiten
            </button>
          </div>
          
          <div v-if="!isEditingEmail" class="email-display">
            <svg class="email-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            <span>{{ user.email }}</span>
          </div>

          <div v-else class="email-edit-form">
            <div class="input-group">
              <label for="email">Neue E-Mail Adresse</label>
              <input 
                id="email"
                v-model="newEmail" 
                type="email" 
                placeholder="neue@email.com"
                @keyup.enter="saveEmail"
              />
            </div>
            <div class="form-actions">
              <button @click="saveEmail" class="btn primary" :disabled="isSaving">
                <span v-if="!isSaving">Speichern</span>
                <span v-else>Speichert...</span>
              </button>
              <button @click="cancelEditEmail" class="btn ghost">Abbrechen</button>
            </div>
          </div>
        </div>

        <!-- Additional Profile Info -->
        <div class="info-section" v-if="user.role === 'startup'">
          <h3 class="section-heading">Startup Informationen</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Pitches erstellt</span>
              <span class="info-value highlight">{{ stats.pitchCount }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Events organisiert</span>
              <span class="info-value highlight">{{ stats.eventCount }}</span>
            </div>
          </div>
        </div>

        <div class="info-section" v-else>
          <h3 class="section-heading">Investor Aktivität</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Gespeicherte Pitches</span>
              <span class="info-value highlight">{{ stats.savedPitches }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Events besucht</span>
              <span class="info-value highlight">{{ stats.eventsAttended }}</span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="profile-actions">
          <button @click="handleLogout" class="btn danger-outline">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            Abmelden
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '~/stores/auth';

const user = ref({ 
  username: '', 
  email: '', 
  role: '',
  date_joined: ''
});

const stats = ref({
  pitchCount: 0,
  eventCount: 0,
  savedPitches: 0,
  eventsAttended: 0
});

const isEditingEmail = ref(false);
const newEmail = ref('');
const isSaving = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

// Avatar URL basierend auf Username
const avatarUrl = computed(() => {
  const seed = user.value.username || 'user';
  return `https://api.dicebear.com/7.x/avataaars/svg?seed=${seed}`;
});

// Formatiertes Beitrittsdatum
const formattedJoinDate = computed(() => {
  if (!user.value.date_joined) return 'Unbekannt';
  const date = new Date(user.value.date_joined);
  return date.toLocaleDateString('de-DE', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
});

// Email bearbeiten
const startEditEmail = () => {
  newEmail.value = user.value.email;
  isEditingEmail.value = true;
  errorMessage.value = '';
  successMessage.value = '';
};

const cancelEditEmail = () => {
  isEditingEmail.value = false;
  newEmail.value = '';
  errorMessage.value = '';
};

const saveEmail = async () => {
  if (!newEmail.value || !newEmail.value.includes('@')) {
    errorMessage.value = 'Bitte geben Sie eine gültige E-Mail Adresse ein.';
    return;
  }

  if (newEmail.value === user.value.email) {
    errorMessage.value = 'Die neue E-Mail ist identisch mit der aktuellen.';
    return;
  }

  isSaving.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const token = localStorage.getItem('access_token');
    const response = await fetch('http://127.0.0.1:8000/api/users/update-email/', {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email: newEmail.value })
    });

    if (response.ok) {
      const data = await response.json();
      user.value.email = newEmail.value;
      isEditingEmail.value = false;
      successMessage.value = 'E-Mail Adresse erfolgreich aktualisiert!';
      
      // Clear success message after 5 seconds
      setTimeout(() => {
        successMessage.value = '';
      }, 5000);
    } else {
      const errorData = await response.json();
      errorMessage.value = errorData.error || 'Fehler beim Aktualisieren der E-Mail Adresse.';
    }
  } catch (error) {
    console.error('Fehler beim Speichern der E-Mail:', error);
    errorMessage.value = 'Netzwerkfehler. Bitte versuchen Sie es später erneut.';
  } finally {
    isSaving.value = false;
  }
};

// Logout
const auth = useAuthStore();
const handleLogout = () => {
  if (confirm('Möchten Sie sich wirklich abmelden?')) {
    auth.logout();
    navigateTo('/login');
  }
};

// Statistiken laden
const loadStats = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  try {
    const apiBase = 'http://127.0.0.1:8000/api';
    
    if (user.value.role === 'startup') {
      // Lade Pitches
      const pitchRes = await fetch(`${apiBase}/pitches/?mine=true`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (pitchRes.ok) {
        const pitches = await pitchRes.json();
        stats.value.pitchCount = pitches.length;
      }

      // Lade Events
      const eventRes = await fetch(`${apiBase}/events/?mine=true`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (eventRes.ok) {
        const events = await eventRes.json();
        stats.value.eventCount = events.length;
      }
    } else {
      // Lade gespeicherte Pitches für Investoren
      const savedRes = await fetch(`${apiBase}/saved-pitches/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (savedRes.ok) {
        const saved = await savedRes.json();
        stats.value.savedPitches = saved.length;
      }

      // Events Attended (Placeholder - würde eine Backend-Erweiterung benötigen)
      stats.value.eventsAttended = 0;
    }
  } catch (err) {
    console.error('Fehler beim Laden der Statistiken:', err);
  }
};

// Initial laden
onMounted(async () => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (!token) {
    navigateTo('/login');
    return;
  }
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/users/me/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (!response.ok) {
      navigateTo('/login');
      return;
    }
    
    const data = await response.json();
    user.value = {
      username: data.username ?? '',
      email: data.email ?? '',
      role: data.profile?.role ?? data.role ?? '',
      date_joined: data.date_joined ?? ''
    };

    // Lade Statistiken
    await loadStats();
  } catch (err) {
    console.error('Fehler beim Laden der Profildaten:', err);
    navigateTo('/login');
  }
});
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* Header */
.profile-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
  color: #fff;
}

.role-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: capitalize;
}

.role-badge.startup {
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: #021;
}

.role-badge.investor {
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
}

/* Alerts */
.alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 1rem 1.25rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  animation: slideIn 0.3s ease;
}

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.alert-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Profile Card */
.profile-card {
  padding: 2rem;
}

.profile-avatar-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 2rem;
}

.avatar-wrapper {
  position: relative;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 3px solid rgba(94, 234, 212, 0.3);
  object-fit: cover;
}

.avatar-badge {
  position: absolute;
  bottom: -4px;
  right: -4px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  border: 2px solid var(--bg);
}

.avatar-badge.startup {
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
}

.avatar-badge.investor {
  background: linear-gradient(135deg, #10b981, #059669);
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  color: #fff;
}

.profile-role {
  font-size: 1rem;
  color: var(--muted);
  margin: 0;
}

/* Info Sections */
.info-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.info-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-heading {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  color: #fff;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-label {
  font-size: 0.85rem;
  color: var(--muted);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 1.1rem;
  color: #fff;
  font-weight: 600;
}

.info-value.highlight {
  color: var(--accent);
  font-size: 1.5rem;
  font-weight: 700;
}

/* Email Section */
.email-display {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  color: #fff;
}

.email-icon {
  width: 20px;
  height: 20px;
  color: var(--accent);
  flex-shrink: 0;
}

.btn-edit {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0.5rem 1rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: var(--accent);
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-edit:hover {
  background: rgba(94, 234, 212, 0.1);
  border-color: rgba(94, 234, 212, 0.3);
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.email-edit-form {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 1rem;
}

/* Actions */
.profile-actions {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.danger-outline {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #ef4444;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.danger-outline:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
}

/* Responsive */
@media (max-width: 640px) {
  .profile-page {
    padding: 1rem 0.5rem;
  }

  .profile-card {
    padding: 1.5rem;
  }

  .profile-avatar-section {
    flex-direction: column;
    text-align: center;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions .btn {
    width: 100%;
  }
}
</style>