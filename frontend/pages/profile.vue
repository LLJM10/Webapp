<template>
  <section id="page-profile" class="profile-page">
    <div class="profile-header-bar">
      <h2 class="page-title">Profil bearbeiten</h2>
      <div class="role-badge" :class="user.role">{{ capitalizedRole }}</div>
    </div>

    <div class="profile-grid">
      <!-- Hauptinformationen -->
      <div class="left-column">
        <!-- Profilbild/Logo Upload Section -->
        <div class="card profile-image-section">
          <div class="image-upload-area">
            <img :src="profileImage" :alt="profileName" class="profile-image" />
            <button class="btn ghost upload-btn">
              <span class="icon">📷</span> Bild ändern
            </button>
          </div>
        </div>

        <!-- Hauptinformationen -->
        <div class="card main-info">
          <div class="section-title">
            <h3>{{ isStartup ? 'Unternehmensinformationen' : 'Investorenprofil' }}</h3>
            <button class="btn primary save-btn" @click="saveProfile">Speichern</button>
          </div>

          <!-- Gemeinsame Felder -->
          <div class="input-group">
            <label>{{ isStartup ? 'Unternehmensname' : 'Name/Organisation' }}</label>
            <input v-model="profile.name" type="text" :placeholder="isStartup ? 'Ihre Firma GmbH' : 'Name oder Organisationsname'" />
          </div>

          <!-- Startup-spezifische Felder -->
          <template v-if="isStartup">
            <div class="input-grid">
              <div class="input-group">
                <label>Branche</label>
                <select v-model="profile.industry">
                  <option value="">Bitte wählen</option>
                  <option v-for="industry in industries" :key="industry" :value="industry">{{ industry }}</option>
                </select>
              </div>
              <div class="input-group">
                <label>Phase</label>
                <select v-model="profile.stage">
                  <option value="">Bitte wählen</option>
                  <option v-for="stage in stages" :key="stage" :value="stage">{{ stage }}</option>
                </select>
              </div>
            </div>
            <div class="input-grid">
              <div class="input-group">
                <label>Mitarbeiterzahl</label>
                <input v-model="profile.employeeCount" type="number" min="1" />
              </div>
              <div class="input-group">
                <label>Gründungsjahr</label>
                <input v-model="profile.foundingYear" type="number" :max="currentYear" />
              </div>
            </div>
          </template>

          <!-- Investor-spezifische Felder -->
          <template v-else>
            <div class="input-grid">
              <div class="input-group">
                <label>Investmentfokus</label>
                <select v-model="profile.investmentFocus" multiple>
                  <option v-for="focus in investmentFoci" :key="focus" :value="focus">{{ focus }}</option>
                </select>
              </div>
              <div class="input-group">
                <label>Ticketgröße</label>
                <select v-model="profile.ticketSize">
                  <option value="">Bitte wählen</option>
                  <option v-for="size in ticketSizes" :key="size" :value="size">{{ size }}</option>
                </select>
              </div>
            </div>
          </template>

          <!-- Gemeinsame Felder -->
          <div class="input-group">
            <label>Kurzbeschreibung</label>
            <textarea 
              v-model="profile.description" 
              :placeholder="isStartup ? 'Beschreiben Sie Ihr Unternehmen kurz...' : 'Beschreiben Sie Ihre Investmentstrategie...'"
              rows="3">
            </textarea>
          </div>
        </div>

        <!-- Dokumente Section -->
        <div class="card documents-section">
          <h3>Dokumente</h3>
          <div class="documents-grid">
            <!-- Startup-spezifische Dokumente -->
            <template v-if="isStartup">
              <div class="document-upload" v-for="doc in startupDocs" :key="doc.type">
                <div class="doc-info">
                  <span class="icon">📄</span>
                  <div>
                    <div class="doc-title">{{ doc.title }}</div>
                    <div class="doc-status" :class="{ 'uploaded': doc.uploaded }">
                      {{ doc.uploaded ? 'Hochgeladen' : 'Noch nicht hochgeladen' }}
                    </div>
                  </div>
                </div>
                <button class="btn ghost">{{ doc.uploaded ? 'Aktualisieren' : 'Hochladen' }}</button>
              </div>
            </template>
            <!-- Investor-spezifische Dokumente -->
            <template v-else>
              <div class="document-upload" v-for="doc in investorDocs" :key="doc.type">
                <div class="doc-info">
                  <span class="icon">📄</span>
                  <div>
                    <div class="doc-title">{{ doc.title }}</div>
                    <div class="doc-status" :class="{ 'uploaded': doc.uploaded }">
                      {{ doc.uploaded ? 'Hochgeladen' : 'Noch nicht hochgeladen' }}
                    </div>
                  </div>
                </div>
                <button class="btn ghost">{{ doc.uploaded ? 'Aktualisieren' : 'Hochladen' }}</button>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="aside-column">
        <!-- Kontaktinformationen -->
        <div class="card contact-info">
          <h3>Kontaktinformationen</h3>
          <div class="input-group">
            <label>E-Mail</label>
            <div class="muted email-display">{{ user.email }}</div>
          </div>
          <div class="input-group">
            <label>Telefon</label>
            <input v-model="profile.phone" type="tel" placeholder="+49" />
          </div>
          <div class="input-group">
            <label>Website</label>
            <input v-model="profile.website" type="url" placeholder="https://" />
          </div>
        </div>

        <!-- Account Actions -->
        <div class="card account-actions">
          <h3>Account</h3>
          <button class="btn danger" @click="handleLogout">Abmelden</button>
        </div>
      </aside>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '~/stores/auth';

const user = ref({ username: '', email: '', role: '' });
const profile = ref({
  name: '',
  industry: '',
  stage: '',
  employeeCount: null,
  foundingYear: null,
  investmentFocus: [],
  ticketSize: '',
  description: '',
  phone: '',
  website: '',
});

// Computed Properties
const isStartup = computed(() => user.value.role === 'startup');
const capitalizedRole = computed(() => user.value.role.charAt(0).toUpperCase() + user.value.role.slice(1));
const currentYear = new Date().getFullYear();

// Konstanten für Auswahlfelder
const industries = [
  'FinTech',
  'HealthTech',
  'CleanTech',
  'AI/ML',
  'SaaS',
  'E-Commerce',
  'IoT',
  'Biotech',
  'Mobility',
  'EdTech'
];

const stages = [
  'Pre-Seed',
  'Seed',
  'Series A',
  'Series B',
  'Series C',
  'Growth'
];

const investmentFoci = [
  'B2B SaaS',
  'DeepTech',
  'FinTech',
  'HealthTech',
  'CleanTech',
  'Consumer',
  'Hardware',
  'Marketplace'
];

const ticketSizes = [
  '< 100k €',
  '100k € - 500k €',
  '500k € - 1M €',
  '1M € - 3M €',
  '> 3M €'
];

const startupDocs = [
  { type: 'pitch_deck', title: 'Pitch Deck', uploaded: false },
  { type: 'financials', title: 'Financial Report', uploaded: false },
  { type: 'cap_table', title: 'Cap Table', uploaded: false },
  { type: 'business_plan', title: 'Business Plan', uploaded: false }
];

const investorDocs = [
  { type: 'credentials', title: 'Investorencredentials', uploaded: false },
  { type: 'portfolio', title: 'Portfolioübersicht', uploaded: false }
];

// Profilbild
const profileImage = ref('https://picsum.photos/seed/profile/200/200');

// Methods
const saveProfile = async () => {
  try {
    const token = localStorage.getItem('access_token');
    const response = await fetch('http://127.0.0.1:8000/users/profile/', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(profile.value)
    });
    if (response.ok) {
      // TODO: Erfolgsmeldung anzeigen
    }
  } catch (error) {
    console.error('Fehler beim Speichern des Profils:', error);
  }
};

// Logout Handler
const auth = useAuthStore();
const handleLogout = () => {
  auth.logout();
  navigateTo('/login');
};

// Initial Data Loading
onMounted(async () => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (!token) return;
  
  try {
    const response = await fetch('http://127.0.0.1:8000/users/me/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) return;
    
    const data = await response.json();
    user.value = {
      username: data.username ?? '',
      email: data.email ?? '',
      role: data.profile?.role ?? data.role ?? ''
    };

    // Lade Profildaten
    if (data.profile) {
      profile.value = {
        ...profile.value,
        ...data.profile
      };
    }
  } catch (err) {
    console.error('Fehler beim Laden der Profildaten:', err);
  }
});
</script>

<style scoped>
.profile-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  margin: 0;
}

.role-badge {
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-weight: 600;
  font-size: 0.9rem;
}

.role-badge.startup {
  background: var(--accent);
  color: #fff;
}

.role-badge.investor {
  background: #4CAF50;
  color: #fff;
}

.profile-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 2rem;
  align-items: start;
}

.profile-image-section {
  text-align: center;
  padding: 2rem;
}

.image-upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.profile-image {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--accent);
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title h3 {
  margin: 0;
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--muted);
}

.input-group input,
.input-group select,
.input-group textarea {
  width: 100%;
  padding: 0.8rem;
  border-radius: var(--radius);
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.03);
  color: #fff;
  font-size: 1rem;
}

.input-group textarea {
  resize: vertical;
  min-height: 100px;
}

.input-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.documents-section {
  margin-top: 2rem;
}

.documents-grid {
  display: grid;
  gap: 1rem;
}

.document-upload {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius);
}

.doc-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.doc-title {
  font-weight: 600;
}

.doc-status {
  font-size: 0.9rem;
  color: var(--muted);
}

.doc-status.uploaded {
  color: #4CAF50;
}

.contact-info,
.account-actions {
  margin-bottom: 1rem;
}

.email-display {
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius);
}

.danger {
  background: #f44336;
  color: white;
}

.danger:hover {
  background: #d32f2f;
}

.icon {
  font-size: 1.2rem;
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
  
  .input-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .profile-header-bar {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .profile-page {
    padding: 1rem;
  }
  
  .section-title {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .save-btn {
    width: 100%;
  }
}
</style>