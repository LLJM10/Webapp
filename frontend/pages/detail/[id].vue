<template>
  <section id="page-detail">
    <div v-if="pitch">
      <!-- Back Button -->
      <div style="margin-bottom: 24px">
        <NuxtLink to="/market" class="btn ghost" style="display:inline-flex;align-items:center;gap:8px">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/>
          </svg>
          Zurück zum Marktplatz
        </NuxtLink>
      </div>

      <!-- Hero Section -->
      <div class="hero-section">
        <img :src="getImageUrl(pitch.img, pitch.title)" :alt="pitch.title" class="hero-image" />
        <div class="hero-overlay">
          <div class="hero-content">
            <h1 class="hero-title">{{ pitch.title }}</h1>
            <div class="hero-meta">
              <span class="badge">{{ pitch.sector }}</span>
              <span class="badge">{{ pitch.stage }}</span>
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
            <h2 style="margin-bottom: 16px">Über das Projekt</h2>
            <p style="font-size: 1.125rem; line-height: 1.75; color: var(--muted)">
              {{ pitch.desc }}
            </p>
          </div>

          <!-- Key Metrics -->
          <div class="card metrics-card">
            <h2 style="margin-bottom: 24px">Investitions-Details</h2>
            <div class="metrics-grid">
              <div class="metric-item">
                <div class="metric-icon">💰</div>
                <div>
                  <div class="metric-label">Funding Ziel</div>
                  <div class="metric-value">{{ pitch.goal }}€</div>
                </div>
              </div>
              <div class="metric-item">
                <div class="metric-icon">📊</div>
                <div>
                  <div class="metric-label">Equity</div>
                  <div class="metric-value">{{ pitch.equity }}%</div>
                </div>
              </div>
              <div v-if="pitch.valuation" class="metric-item">
                <div class="metric-icon">💎</div>
                <div>
                  <div class="metric-label">Bewertung</div>
                  <div class="metric-value">{{ pitch.valuation }}</div>
                </div>
              </div>
              <div class="metric-item">
                <div class="metric-icon">🚀</div>
                <div>
                  <div class="metric-label">Stage</div>
                  <div class="metric-value">{{ pitch.stage }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Documents Section -->
          <div v-if="pitch.pitch_deck || pitch.business_plan || pitch.financial_report" class="card documents-card">
            <h2 style="margin-bottom: 24px">📎 Dokumente</h2>
            <div class="documents-grid">
              <a v-if="pitch.pitch_deck" 
                 :href="pitch.pitch_deck" 
                 target="_blank" 
                 class="document-item">
                <div class="document-icon">📄</div>
                <div>
                  <div class="document-title">Pitch Deck</div>
                  <div class="document-subtitle">PDF Dokument</div>
                </div>
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                  <path d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5z"/>
                  <path d="M16 .5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h3.793L6.146 9.146a.5.5 0 1 0 .708.708L15 1.707V5.5a.5.5 0 0 0 1 0v-5z"/>
                </svg>
              </a>
              <a v-if="pitch.business_plan" 
                 :href="pitch.business_plan" 
                 target="_blank" 
                 class="document-item">
                <div class="document-icon">📊</div>
                <div>
                  <div class="document-title">Business Plan</div>
                  <div class="document-subtitle">PDF Dokument</div>
                </div>
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                  <path d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5z"/>
                  <path d="M16 .5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h3.793L6.146 9.146a.5.5 0 1 0 .708.708L15 1.707V5.5a.5.5 0 0 0 1 0v-5z"/>
                </svg>
              </a>
              <a v-if="pitch.financial_report" 
                 :href="pitch.financial_report" 
                 target="_blank" 
                 class="document-item">
                <div class="document-icon">💰</div>
                <div>
                  <div class="document-title">Financial Report</div>
                  <div class="document-subtitle">PDF Dokument</div>
                </div>
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                  <path d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5z"/>
                  <path d="M16 .5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h3.793L6.146 9.146a.5.5 0 1 0 .708.708L15 1.707V5.5a.5.5 0 0 0 1 0v-5z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>

        <!-- Right Column: Sidebar -->
        <aside class="sidebar">
          <!-- CTA Card -->
          <div class="card cta-card">
            <h3 style="margin-bottom: 16px; font-size: 1.25rem">Interessiert?</h3>
            <p class="muted" style="margin-bottom: 20px; font-size: 0.95rem">
              Investiere in dieses vielversprechende Startup und werde Teil der Erfolgsgeschichte.
            </p>
            <PaymentButton v-if="pitch && isInvestor" :amount="paymentAmount" label="Jetzt investieren" style="width: 100%; margin-bottom: 12px" />
            <button 
              v-if="isInvestor" 
              class="btn ghost" 
              style="width: 100%; margin-bottom: 12px" 
              @click="toggleSavePitch"
              :disabled="isLoading"
            >
              <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px">
                <path v-if="isSaved" d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2z"/>
                <path v-else d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1H4z"/>
              </svg>
              {{ isSaved ? '★ Gemerkt' : '☆ Pitch merken' }}
            </button>
            <button @click="openMail" class="btn ghost" style="width: 100%">
              Kontakt aufnehmen
            </button>
          </div>

          <!-- Info Card -->
          <div class="card info-card">
            <h3 style="margin-bottom: 16px; font-size: 1.1rem">Weitere Informationen</h3>
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">Sektor</span>
                <span class="info-value">{{ pitch.sector }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Stage</span>
                <span class="info-value">{{ pitch.stage }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Funding Ziel</span>
                <span class="info-value">{{ pitch.goal }}€</span>
              </div>
              <div class="info-item">
                <span class="info-label">Equity</span>
                <span class="info-value">{{ pitch.equity }}%</span>
              </div>
              <div v-if="pitch.valuation" class="info-item">
                <span class="info-label">Bewertung</span>
                <span class="info-value">{{ pitch.valuation }}</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
    <div v-else>
      <div class="card" style="text-align: center; padding: 48px; margin-top: 48px">
        <h2>Pitch nicht gefunden</h2>
        <p class="muted" style="margin-top: 16px">
          Dieser Pitch existiert nicht oder wurde entfernt.
        </p>
        <NuxtLink to="/market" class="btn primary" style="margin-top: 24px">
          Zurück zum Marktplatz
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useRuntimeConfig } from '#app';
import { dummyApi } from '~/composables/useDemoData';
import PaymentButton from '~/components/PaymentButton.vue';

const route = useRoute();
const pitch = ref(null);
const paymentAmount = ref('10.00');
const user = ref({ username: '', email: '', role: 'startup' }); // Default user object
const isSaved = ref(false); // Track if pitch is saved
const isLoading = ref(false); // Track button loading state

// Computed property to check if user is an investor
const isInvestor = computed(() => user.value.role === 'investor');


function openMail() {
  window.location.href = 'mailto:startup@test.de'
}

// Helper function to get the correct image URL
function getImageUrl(imgPath, fallbackText = 'Pitch') {
  if (!imgPath) {
    return 'https://placehold.co/1200x400/3b82f6/ffffff?text=' + encodeURIComponent(fallbackText);
  }
  
  // If it's already a full URL (http/https), return as is
  if (imgPath.startsWith('http://') || imgPath.startsWith('https://')) {
    return imgPath;
  }
  
  // If it's a relative path from backend (e.g., /media/pitch_images/...)
  if (imgPath.startsWith('/media/')) {
    const config = useRuntimeConfig();
    const apiBase = config.public?.apiBase || 'http://127.0.0.1:8000';
    return apiBase + imgPath;
  }
  
  // If it's just a filename or relative path without /media/
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase || 'http://127.0.0.1:8000';
  return `${apiBase}/media/${imgPath}`;
}

// Toggle save/unsave pitch
async function toggleSavePitch() {
  if (!pitch.value || !user.value || user.value.role !== 'investor') return;
  
  isLoading.value = true;
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (!token) {
    alert('Bitte melde dich an, um Pitches zu speichern.');
    isLoading.value = false;
    return;
  }
  
  try {
    const endpoint = isSaved.value ? 'unsave_pitch' : 'save_pitch';
    const res = await fetch(`${apiBase}/saved-pitches/${endpoint}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ pitch_id: pitch.value.id })
    });
    
    if (res.ok) {
      isSaved.value = !isSaved.value;
      console.log(isSaved.value ? 'Pitch saved' : 'Pitch unsaved');
    } else {
      const errorData = await res.json();
      console.error('Error toggling saved pitch:', errorData);
      alert('Fehler beim Speichern des Pitches.');
    }
  } catch (e) {
    console.error('Error saving pitch:', e);
    alert('Fehler beim Speichern des Pitches.');
  } finally {
    isLoading.value = false;
  }
}

// Check if pitch is already saved
async function checkIfSaved() {
  if (!pitch.value || !user.value || user.value.role !== 'investor') return;
  
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (!token) return;
  
  try {
    const res = await fetch(`${apiBase}/saved-pitches/check_saved/?pitch_id=${pitch.value.id}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (res.ok) {
      const data = await res.json();
      isSaved.value = data.saved;
    }
  } catch (e) {
    console.error('Error checking saved status:', e);
  }
}

onMounted(async () => {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const pitchId = route.params.id;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  // Load user data from backend
  if (token) {
    try {
      const userRes = await fetch('http://127.0.0.1:8000/api/users/me/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (userRes.ok) {
        const userData = await userRes.json();
        user.value.username = userData.username || '';
        user.value.email = userData.email || '';
        user.value.role = userData.profile?.role || userData.role || 'startup';
        console.log('User loaded:', user.value);
      } else {
        console.warn('Failed to load user data:', userRes.status);
      }
    } catch (e) {
      console.error('Error loading user:', e);
    }
  }

  // Load pitch data
  if (apiBase && pitchId) {
    try {
      const res = await fetch(`${apiBase}/pitches/${pitchId}/`, {
        headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) }
      });
      
      if (res.ok) {
        pitch.value = await res.json();
        console.log('Pitch loaded:', pitch.value);
        
        // Parse funding goal for payment amount
        const numeric = pitch.value?.goal?.toString().replace(/[€ ,]/g, '') || '';
        const parsed = parseFloat(numeric) || 10.00;
        paymentAmount.value = parsed.toFixed(2);
      } else {
        console.error('Failed to load pitch:', res.status);
      }
    } catch (e) {
      console.error('Error loading pitch:', e);
    }
  }
  
  // Check if pitch is saved after loading
  if (pitch.value && user.value.role === 'investor') {
    await checkIfSaved();
  }
});
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
.metrics-card,
.documents-card,
.cta-card,
.info-card {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  padding: 32px;
  border-radius: 12px;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.metric-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px;
  background: rgba(94, 234, 212, 0.05);
  border: 1px solid rgba(94, 234, 212, 0.1);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.metric-item:hover {
  background: rgba(94, 234, 212, 0.08);
  border-color: rgba(94, 234, 212, 0.2);
  transform: translateY(-2px);
}

.metric-icon {
  font-size: 2rem;
  line-height: 1;
}

.metric-label {
  color: var(--muted);
  font-size: 0.875rem;
  margin-bottom: 4px;
}

.metric-value {
  color: var(--accent);
  font-size: 1.5rem;
  font-weight: 700;
}

/* Documents Grid */
.documents-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.document-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
}

.document-item:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: var(--accent);
  transform: translateX(4px);
}

.document-icon {
  font-size: 2rem;
  line-height: 1;
}

.document-title {
  font-weight: 600;
  font-size: 1.05rem;
  margin-bottom: 4px;
}

.document-subtitle {
  color: var(--muted);
  font-size: 0.875rem;
}

.document-item svg {
  margin-left: auto;
  color: var(--accent);
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.document-item:hover svg {
  opacity: 1;
}

/* Info List */
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
  
  .metrics-grid {
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
  .metrics-card,
  .documents-card,
  .cta-card,
  .info-card {
    padding: 24px;
  }
}
</style>