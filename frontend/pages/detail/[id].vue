<template>
  <section id="page-detail">
    <!-- Investment Modal -->
    <div v-if="showInvestmentModal" class="modal-overlay" @click.self="showInvestmentModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Investment Details</h3>
          <button @click="showInvestmentModal = false" class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <p class="muted mb-16">Investiere in <strong>{{ pitch?.title }}</strong></p>
          <div class="info-display">
            <div class="info-row">
              <span class="info-label">Investitionsbetrag:</span>
              <span class="info-value">{{ formatCurrency(investmentForm.amount) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Equity Anteil:</span>
              <span class="info-value">{{ investmentForm.equity_percentage }}%</span>
            </div>
          </div>
          <div v-if="investmentError" class="alert alert-error mb-16">
            {{ investmentError }}
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showInvestmentModal = false" class="btn ghost">Abbrechen</button>
          <button @click="submitInvestment" class="btn primary" :disabled="investmentLoading">
            {{ investmentLoading ? 'Wird verarbeitet...' : 'Investieren' }}
          </button>
        </div>
      </div>
    </div>
    
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
            <button 
              v-if="isInvestor" 
              @click="openInvestmentModal" 
              class="btn primary" 
              style="width: 100%; margin-bottom: 12px"
            >
              <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px">
                <path d="M4 10.781c.148 1.667 1.513 2.85 3.591 3.003V15h1.043v-1.216c2.27-.179 3.678-1.438 3.678-3.3 0-1.59-.947-2.51-2.956-3.028l-.722-.187V3.467c1.122.11 1.879.714 2.07 1.616h1.47c-.166-1.6-1.54-2.748-3.54-2.875V1H7.591v1.233c-1.939.23-3.27 1.472-3.27 3.156 0 1.454.966 2.483 2.661 2.917l.61.162v4.031c-1.149-.17-1.94-.8-2.131-1.718H4zm3.391-3.836c-1.043-.263-1.6-.825-1.6-1.616 0-.944.704-1.641 1.8-1.828v3.495l-.2-.05zm1.591 1.872c1.287.323 1.852.859 1.852 1.769 0 1.097-.826 1.828-2.2 1.939V8.73l.348.086z"/>
              </svg>
              Investieren
            </button>
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
import { useRoute, useRouter } from 'vue-router';
import { useRuntimeConfig } from '#app';
import { dummyApi } from '~/composables/useDemoData';
import { usePayPal } from '~/composables/usePayPal';

const route = useRoute();
const router = useRouter();
const pitch = ref(null);
const user = ref({ username: '', email: '', role: 'startup' }); // Default user object
const isSaved = ref(false); // Verfolge ob Pitch gespeichert ist
const isLoading = ref(false); // Verfolge Button-Ladezustand

// Investitionsmodal-Status
const showInvestmentModal = ref(false);
const investmentLoading = ref(false);
const investmentError = ref('');
const investmentForm = ref({
  amount: 50000,
  equity_percentage: 5.0
});

// Berechne, ob Benutzer ein Investor ist
const isInvestor = computed(() => user.value.role === 'investor');

// Investitionsmodal öffnen und Werte vom Pitch initialisieren
function openInvestmentModal() {
  if (!pitch.value) return;
  
  // Investitionsformular mit Pitch-Werten initialisieren
  investmentForm.value.amount = parseFloat(pitch.value.goal) || 50000;
  investmentForm.value.equity_percentage = parseFloat(pitch.value.equity) || 5.0;
  
  // Fehler zurücksetzen und Modal öffnen
  investmentError.value = '';
  showInvestmentModal.value = true;
}

// Hilfsfunktion zur Währungsformatierung
function formatCurrency(value) {
  return new Intl.NumberFormat('de-DE', { 
    style: 'currency', 
    currency: 'EUR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
}

function openMail() {
  window.location.href = 'mailto:startup@test.de'
}

// Hilfsfunktion zum Abrufen der korrekten Bild-URL
function getImageUrl(imgPath, fallbackText = 'Pitch') {
  if (!imgPath) {
    return 'https://placehold.co/1200x400/3b82f6/ffffff?text=' + encodeURIComponent(fallbackText);
  }
  
  // Wenn es bereits eine vollständige URL ist (http/https), direkt zurückgeben
  if (imgPath.startsWith('http://') || imgPath.startsWith('https://')) {
    return imgPath;
  }
  
  // Wenn es ein relativer Pfad vom Backend ist (z.B. /media/pitch_images/...)
  if (imgPath.startsWith('/media/')) {
    const config = useRuntimeConfig();
    const apiBase = config.public?.apiBase || 'http://127.0.0.1:8000';
    return apiBase + imgPath;
  }
  
  // Wenn es nur ein Dateiname oder relativer Pfad ohne /media/ ist
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase || 'http://127.0.0.1:8000';
  return `${apiBase}/media/${imgPath}`;
}

// Pitch speichern/entfernen umschalten
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

// Prüfe ob Pitch bereits gespeichert ist
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

// Investition absenden
async function submitInvestment() {
  if (!pitch.value) return;
  
  investmentError.value = '';
  investmentLoading.value = true;
  
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (!token) {
    investmentError.value = 'Bitte melde dich an, um zu investieren.';
    investmentLoading.value = false;
    return;
  }
  
  // Validation
  if (!investmentForm.value.amount || investmentForm.value.amount <= 0) {
    investmentError.value = 'Bitte gib einen gültigen Betrag ein.';
    investmentLoading.value = false;
    return;
  }
  
  if (!investmentForm.value.equity_percentage || investmentForm.value.equity_percentage <= 0 || investmentForm.value.equity_percentage > 100) {
    investmentError.value = 'Bitte gib einen gültigen Equity-Anteil ein (0-100%).';
    investmentLoading.value = false;
    return;
  }
  
  try {
    // Schritt 1: Investition sofort in Datenbank erstellen
    const res = await fetch(`${apiBase}/investments/invest/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        pitch_id: pitch.value.id,
        amount: investmentForm.value.amount,
        equity_percentage: investmentForm.value.equity_percentage
      })
    });
    
    if (res.ok) {
      const data = await res.json();
      
      // Modal schließen und Erfolg anzeigen
      showInvestmentModal.value = false;
      alert(`Investment erfolgreich gespeichert! (ID: ${data.id})`);
      
      // Schritt 2: PayPal in neuem Tab öffnen (nicht blockierend)
      try {
        const { createOrder } = usePayPal();
        const returnUrl = `${window.location.origin}/dashboard?investment_success=${data.id}`;
        const cancelUrl = `${window.location.origin}/dashboard?investment_id=${data.id}`;
        
        const paypalResp = await createOrder({ 
          amount: investmentForm.value.amount, 
          currency: 'EUR',
          returnUrl,
          cancelUrl
        });
        
        const approval = paypalResp.approval_url || paypalResp.approvalUrl || paypalResp.data?.approval_url;
        if (approval) {
          // PayPal in neuem Tab öffnen
          window.open(approval, '_blank');
        } else {
          console.error('No approval URL from PayPal', paypalResp);
        }
      } catch (paypalError) {
        console.error('PayPal error:', paypalError);
        // Investition ist bereits gespeichert, daher nicht kritisch
      }
      
      // Nach kurzer Verzögerung zum Dashboard weiterleiten
      setTimeout(() => {
        router.push('/dashboard');
      }, 2000);
    } else {
      const errorData = await res.json();
      investmentError.value = errorData.error || errorData.detail || 'Fehler beim Investieren.';
    }
  } catch (e) {
    console.error('Error submitting investment:', e);
    investmentError.value = 'Netzwerkfehler. Bitte versuche es erneut.';
  } finally {
    investmentLoading.value = false;
  }
}

onMounted(async () => {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const pitchId = route.params.id;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  // Benutzerdaten vom Backend laden
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

  // Pitch-Daten laden
  if (apiBase && pitchId) {
    try {
      const res = await fetch(`${apiBase}/pitches/${pitchId}/`, {
        headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) }
      });
      
      if (res.ok) {
        pitch.value = await res.json();
        console.log('Pitch loaded:', pitch.value);
      } else {
        console.error('Failed to load pitch:', res.status);
      }
    } catch (e) {
      console.error('Error loading pitch:', e);
    }
  }
  
  // Prüfe ob Pitch gespeichert ist nach dem Laden
  if (pitch.value && user.value.role === 'investor') {
    await checkIfSaved();
  }
});
</script>

<style scoped>
/* Spezifische Styles für Detail-Seite */

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

/* Documents Grid */
.documents-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* CTA Card */
.cta-card {
  background: linear-gradient(135deg, rgba(94, 234, 212, 0.1) 0%, rgba(96, 165, 250, 0.1) 100%);
  border: 1px solid rgba(94, 234, 212, 0.2);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text);
}

.form-control {
  width: 100%;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.08);
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
}

@media (max-width: 768px) {
  .description-card,
  .metrics-card,
  .documents-card,
  .cta-card,
  .info-card {
    padding: 24px;
  }
}
</style>