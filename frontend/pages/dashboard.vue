<template>
  <section id="page-dashboard">
    <AiDescriptionModal 
      :is-open="showAiModal"
      type="event"
      @close="showAiModal = false"
      @generated="handleAiGenerated"
    />
    
    <!-- Dashboard Header -->
    <div class="dashboard-header">
      <div>
        <h2 class="mb-8">Dashboard</h2>
        <p class="muted">Willkommen zurück, {{ user.username }}</p>
      </div>
    </div>

    <!-- START: Nur für Startup-Rolle -->
    <div v-if="user.role === 'startup'" class="dashboard-layout">
      
      <!-- Hauptbereich: 2-Spalten Layout -->
      <div class="dashboard-main">
        
        <!-- Linke Spalte: Pitches -->
        <div class="dashboard-section">
          <div class="section-header">
            <div>
              <h3>Meine Pitches</h3>
              <p class="muted">Verwalte deine Angebote und Kontakte</p>
            </div>
            <NuxtLink to="/pitches/formular" class="btn primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
              </svg>
              Neues Angebot
            </NuxtLink>
          </div>

          <div class="pitches-grid">
            <!-- Bestehende Pitches mit Edit/Delete Buttons -->
            <div v-for="pitch in myPitches" :key="pitch.id" class="pitch-card">
              <img :src="getImageUrl(pitch.img, pitch.title)" :alt="pitch.title" class="pitch-image">
              <div class="pitch-content">
                <div class="pitch-header">
                  <h4>{{ pitch.title }}</h4>
                  <div class="pitch-meta">
                    <span class="badge-pill">{{ pitch.sector }}</span>
                    <span class="badge-pill">{{ pitch.stage }}</span>
                  </div>
                </div>
                <p class="muted pitch-desc">{{ truncateText(pitch.desc, 50) }}</p>
                
                <div class="pitch-stats">
                  <div class="stat-item">
                    <span class="stat-label">Ziel</span>
                    <span class="stat-value">{{ pitch.goal }}€</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Equity</span>
                    <span class="stat-value">{{ pitch.equity }}%</span>
                  </div>
                </div>
                
                <!-- PDF Dokumente -->
                <div v-if="pitch.pitch_deck || pitch.business_plan || pitch.financial_report" class="pitch-documents">
                  <div class="doc-label">📎 Dokumente</div>
                  <div class="doc-links">
                    <a v-if="pitch.pitch_deck" :href="pitch.pitch_deck" target="_blank" class="doc-link">📄 Deck</a>
                    <a v-if="pitch.business_plan" :href="pitch.business_plan" target="_blank" class="doc-link">📊 Plan</a>
                    <a v-if="pitch.financial_report" :href="pitch.financial_report" target="_blank" class="doc-link">💰 Report</a>
                  </div>
                </div>
                
                <div class="pitch-actions">
                  <NuxtLink :to="`/pitches/formular?id=${pitch.id}`" class="btn-small ghost">Bearbeiten</NuxtLink>
                  <button class="btn-small danger-outline" @click="confirmDeletePitch(pitch)">Löschen</button>
                </div>

                <!-- Delete Confirmation (inline) -->
                <div v-if="pitchToDelete?.id === pitch.id" class="delete-confirmation">
                  <strong class="text-danger">Wirklich löschen?</strong>
                  <p class="mt-8 text-muted">Dieser Pitch wird dauerhaft gelöscht.</p>
                  <div class="flex gap-8 mt-12">
                    <button class="btn danger small" @click="deletePitch">Ja, löschen</button>
                    <button class="btn ghost small" @click="cancelDeletePitch">Abbrechen</button>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="!myPitches.length" class="empty-state">
              <div class="empty-icon">📊</div>
              <p class="empty-text">Noch keine Angebote erstellt</p>
              <NuxtLink to="/pitches/formular" class="btn primary empty-cta">
                Erstes Angebot anlegen
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Rechte Spalte: Events -->
        <div class="dashboard-section">
          <div class="section-header">
            <div>
              <h3>Meine Events</h3>
              <p class="muted">Verwalte deine geplanten Events</p>
            </div>
            <NuxtLink to="/events/formular" class="btn primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
              </svg>
              Neues Event
            </NuxtLink>
          </div>

          <div class="events-list">
            <div v-for="event in myEvents" :key="event.id" class="event-card">
              <img :src="event.img || 'https://picsum.photos/seed/event/900/480'" :alt="event.name" class="event-image">
              <div class="event-content">
                <h4>{{ event.name }}</h4>
                <div class="event-meta">
                  <span>📅 {{ formatEventDate(event.date) }}</span>
                  <span>📍 {{ event.location }}</span>
                </div>
                <p class="muted event-desc">{{ truncateText(event.description, 50) }}</p>
                <div class="event-actions">
                  <NuxtLink :to="`/events/formular?id=${event.id}`" class="btn-small ghost">Bearbeiten</NuxtLink>
                  <button class="btn-small danger-outline" @click="confirmDeleteEvent(event)">Löschen</button>
                </div>

                <!-- Delete Confirmation (inline) -->
                <div v-if="eventToDelete?.id === event.id" class="delete-confirmation">
                  <strong class="text-danger">Wirklich löschen?</strong>
                  <p class="mt-8 text-muted">Dieses Event wird dauerhaft gelöscht.</p>
                  <div class="flex gap-8 mt-12">
                    <button class="btn danger small" @click="deleteEvent">Ja, löschen</button>
                    <button class="btn ghost small" @click="cancelDeleteEvent">Abbrechen</button>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="!myEvents.length" class="empty-state">
              <div class="empty-icon">📅</div>
              <p class="empty-text">Noch keine Events erstellt</p>
              <NuxtLink to="/events/formular" class="btn primary empty-cta">
                Erstes Event erstellen
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar: Nutzerinfo & Matching -->
      <aside class="dashboard-sidebar">
        <div class="sidebar-card">
          <h3>Nutzerinfo</h3>
          <div class="user-info">
            <div class="info-row">
              <span class="info-label">Benutzername</span>
              <span class="info-value">{{ user.username }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">E-Mail</span>
              <span class="info-value">{{ user.email }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Rolle</span>
              <span class="info-value">{{ user.role }}</span>
            </div>
          </div>
        </div>

        <div class="sidebar-card">
          <h3>Matching Vorschläge</h3>
          <div class="match-item">
            <div class="match-avatar">AM</div>
            <div>
              <div class="match-name">Anna Müller</div>
              <div class="muted" style="font-size: 0.875rem">Interesse: Energy</div>
            </div>
          </div>
        </div>
      </aside>

    </div>
    <!-- ENDE: Nur für Startup-Rolle -->

    <!-- Investor Dashboard - Nur für Investor-Rolle -->
    <div v-else-if="user.role === 'investor'" class="investor-dashboard">
      
      <!-- KPI Overview Grid -->
      <div class="kpi-section">
        <h3 class="section-title">Portfolio Übersicht</h3>
        <div class="kpi-grid">
          <!-- Investiertes Kapital -->
          <div class="kpi-card glow-card">
            <div class="kpi-icon-wrapper primary-glow">
              <svg class="kpi-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
              </svg>
            </div>
            <div class="kpi-content">
              <div class="kpi-label">Investiertes Kapital</div>
              <div class="kpi-value">{{ formatCurrency(investorKPIs.totalInvested) }}</div>
            </div>
          </div>

          <!-- Anzahl Startups -->
          <div class="kpi-card glow-card">
            <div class="kpi-icon-wrapper accent-glow">
              <svg class="kpi-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <div class="kpi-content">
              <div class="kpi-label">Portfolio Startups</div>
              <div class="kpi-value">{{ investorKPIs.startupCount }}</div>
              <div class="kpi-trend neutral">{{ investorKPIs.activeStartups }} aktiv</div>
            </div>
          </div>

          <!-- Watchlist -->
          <div class="kpi-card glow-card">
            <div class="kpi-icon-wrapper warning-glow">
              <svg class="kpi-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
              </svg>
            </div>
            <div class="kpi-content">
              <div class="kpi-label">Watchlist</div>
              <div class="kpi-value">{{ investorKPIs.watchlistCount }}</div>
              <div class="kpi-trend neutral">{{ investorKPIs.newThisWeek }} neu diese Woche</div>
            </div>
          </div>

          <!-- Durchschnitt pro Startup -->
          <div class="kpi-card glow-card">
            <div class="kpi-icon-wrapper success-glow">
              <svg class="kpi-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="8.5" cy="7" r="4"/>
                <line x1="20" y1="8" x2="20" y2="14"/>
                <line x1="23" y1="11" x2="17" y2="11"/>
              </svg>
            </div>
            <div class="kpi-content">
              <div class="kpi-label">Ø Investment</div>
              <div class="kpi-value">{{ formatCurrency(investorKPIs.avgInvestment) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Performance Metrics -->
      <div class="performance-section">
        <h3 class="section-title">Performance Metriken</h3>
        <div class="performance-grid">
          <!-- Rendite Forecast -->
          <div class="metric-card">
            <div class="metric-header">
              <div class="metric-title">
                <svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
                Rendite-Forecast
              </div>
            </div>
            <div class="metric-value-large">{{ formatCurrency(investorKPIs.projectedReturn) }}</div>
            <div class="metric-footer">Prognostiziert bis Ende {{ new Date().getFullYear() + 1 }}</div>
          </div>
        </div>
      </div>

      <!-- Risk Metrics Section (NEW) -->
      <div v-if="investorKPIs.valueAtRisk" class="performance-section">
        <h3 class="section-title">Risiko-Analyse</h3>
        <div class="performance-grid">
          <!-- Value at Risk 95% -->
          <div class="metric-card">
            <div class="metric-header">
              <div class="metric-title">
                <svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
                Value at Risk (95%)
              </div>
              <div class="metric-change" :class="investorKPIs.valueAtRisk.riskLevel === 'Niedrig' ? 'positive' : (investorKPIs.valueAtRisk.riskLevel === 'Mittel' ? 'neutral' : 'negative')">
                {{ investorKPIs.valueAtRisk.riskLevel }}
              </div>
            </div>
            <div class="metric-value-large">{{ formatCurrency(investorKPIs.valueAtRisk.var_95) }}</div>
            <div class="metric-footer">Maximal zu erwartender Verlust (95% Konfidenz)</div>
          </div>

          <!-- Expected Loss -->
          <div class="metric-card">
            <div class="metric-header">
              <div class="metric-title">
                <svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"/>
                  <polyline points="19 12 12 19 5 12"/>
                </svg>
                Expected Loss
              </div>
              <div class="metric-change neutral">VaR × 1.3</div>
            </div>
            <div class="metric-value-large">{{ formatCurrency(investorKPIs.valueAtRisk.expectedLoss) }}</div>
            <div class="metric-footer">Durchschnittlicher Verlust bei Risikoeintritt</div>
          </div>

          <!-- Portfolio Concentration -->
          <div class="metric-card">
            <div class="metric-header">
              <div class="metric-title">
                <svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                </svg>
                Konzentrationsrisiko
              </div>
              <div class="metric-change" :class="investorKPIs.concentrationRisk === 'Niedrig' ? 'positive' : (investorKPIs.concentrationRisk === 'Mittel' ? 'neutral' : 'negative')">
                {{ investorKPIs.concentrationRisk }}
              </div>
            </div>
            <div class="metric-value-large">{{ investorKPIs.herfindahlIndex?.toFixed(3) || '0.000' }}</div>
            <div class="metric-footer">Herfindahl-Hirschman Index (HHI)</div>
          </div>
        </div>
      </div>

      <!-- Matching Vorschläge -->
      <div class="matching-section">
        <div class="section-header-inline">
          <h3 class="section-title">Empfohlene Investments</h3>
          <NuxtLink to="/market" class="link-with-icon">
            Alle ansehen
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </NuxtLink>
        </div>
        <div class="matching-grid">
          <div v-for="match in investorKPIs.matchingSuggestions" :key="match.id" class="matching-card" @click="navigateToDetail(match.id)">
            <div class="matching-header">
              <img :src="getImageUrl(match.img, match.title)" :alt="match.title" class="matching-image">
              <div class="matching-score">
                <svg class="score-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                {{ match.matchScore }}%
              </div>
            </div>
            <div class="matching-content">
              <h4 class="matching-title">{{ match.title }}</h4>
              <div class="matching-meta">
                <span class="meta-tag">{{ match.sector }}</span>
                <span class="meta-tag">{{ match.stage }}</span>
              </div>
              <p class="matching-desc">{{ match.desc }}</p>
              <div class="matching-stats">
                <div class="stat-mini">
                  <span class="stat-mini-label">Ziel</span>
                  <span class="stat-mini-value">{{ match.goal }}€</span>
                </div>
                <div class="stat-mini">
                  <span class="stat-mini-label">Equity</span>
                  <span class="stat-mini-value">{{ match.equity }}%</span>
                </div>
              </div>
              <div class="matching-reason">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                {{ match.matchReason }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="activity-section">
        <h3 class="section-title">Letzte Aktivitäten</h3>
        <div class="activity-list">
          <div v-for="activity in investorKPIs.recentActivity" :key="activity.id" class="activity-item">
            <div class="activity-icon" :class="activity.type">
              <svg v-if="activity.type === 'investment'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
              </svg>
              <svg v-else-if="activity.type === 'watchlist'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
            </div>
            <div class="activity-content">
              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-meta">{{ activity.startup }} • {{ activity.time }}</div>
            </div>
            <div class="activity-amount" v-if="activity.amount">{{ activity.amount }}</div>
          </div>
        </div>
      </div>

      <!-- Gespeicherte Pitches -->
      <div class="saved-pitches-section">
        <h3 class="section-title">Meine gespeicherten Pitches</h3>
        <div v-if="savedPitches.length > 0" class="saved-pitches-grid">
          <div v-for="saved in savedPitches" :key="saved.id" class="saved-pitch-card">
            <NuxtLink :to="`/detail/${saved.pitch.id}`" class="saved-pitch-link">
              <img :src="getImageUrl(saved.pitch.img, saved.pitch.title)" :alt="saved.pitch.title" class="saved-pitch-image">
              <div class="saved-pitch-content">
                <h4 class="saved-pitch-title">{{ saved.pitch.title }}</h4>
                <div class="saved-pitch-meta">
                  <span class="meta-badge">{{ saved.pitch.sector }}</span>
                  <span class="meta-badge">{{ saved.pitch.stage }}</span>
                </div>
                <p class="saved-pitch-desc">{{ truncateText(saved.pitch.desc, 80) }}</p>
                <div class="saved-pitch-stats">
                  <div class="stat-small">
                    <span class="stat-small-label">Ziel</span>
                    <span class="stat-small-value">{{ saved.pitch.goal }}€</span>
                  </div>
                  <div class="stat-small">
                    <span class="stat-small-label">Equity</span>
                    <span class="stat-small-value">{{ saved.pitch.equity }}%</span>
                  </div>
                </div>
              </div>
            </NuxtLink>
            <button class="btn-remove-saved" @click.prevent="removeSavedPitch(saved.pitch.id)" title="Entfernen">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>
        <div v-else class="empty-saved-state">
          <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
          </svg>
          <p class="empty-text">Noch keine Pitches gespeichert</p>
          <NuxtLink to="/market" class="btn primary">Zum Marktplatz</NuxtLink>
        </div>
      </div>

      <!-- Meine Investments (für Testing) -->
      <div class="investments-section" v-if="myInvestments.length > 0">
        <div class="section-header-inline">
          <h3 class="section-title">Meine Investments</h3>
          <span class="badge-count">{{ myInvestments.length }}</span>
        </div>
        <div class="investments-grid">
          <div v-for="investment in myInvestments" :key="investment.id" class="investment-card">
            <div class="investment-header">
              <h4>{{ investment.pitch.title }}</h4>
              <span class="investment-status" :class="investment.status">{{ investment.status }}</span>
            </div>
            <div class="investment-details">
              <div class="detail-row">
                <span class="detail-label">Betrag:</span>
                <span class="detail-value">{{ formatCurrency(investment.amount) }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Equity:</span>
                <span class="detail-value">{{ investment.equity_percentage }}%</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Datum:</span>
                <span class="detail-value">{{ new Date(investment.investment_date).toLocaleDateString('de-DE') }}</span>
              </div>
              <div v-if="investment.roi" class="detail-row">
                <span class="detail-label">ROI:</span>
                <span class="detail-value" :class="investment.roi > 0 ? 'positive' : 'negative'">
                  {{ investment.roi > 0 ? '+' : '' }}{{ investment.roi }}%
                </span>
              </div>
            </div>
            <button class="btn-remove-investment" @click="removeInvestment(investment.id)" title="Investment löschen">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
              Löschen
            </button>
          </div>
        </div>
      </div>

      <!-- NEU: Dokumente / Zertifikate Sektion -->
      <div class="documents-section" v-if="myInvestments.length > 0">
        <div class="section-header-inline">
          <h3 class="section-title">Meine Dokumente & Zertifikate</h3>
          <span class="badge-count">{{ myInvestments.length }}</span>
        </div>
        <p class="section-description">
          Für jedes Investment steht Ihnen ein offizielles Shareholder-Zertifikat zum Download bereit.
        </p>
        
        <div class="documents-grid">
          <div v-for="investment in myInvestments" :key="`doc-${investment.id}`" class="document-card">
            <div class="document-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="12" y1="18" x2="12" y2="12"/>
                <line x1="9" y1="15" x2="15" y2="15"/>
              </svg>
            </div>
            <div class="document-content">
              <h4 class="document-title">Zeichnungsschein</h4>
              <p class="document-startup">{{ investment.pitch.title }}</p>
              <div class="document-meta">
                <span class="meta-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                  {{ new Date(investment.investment_date).toLocaleDateString('de-DE') }}
                </span>
                <span class="meta-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="12" y1="1" x2="12" y2="23"/>
                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                  </svg>
                  {{ formatCurrency(investment.amount) }}
                </span>
              </div>
            </div>
            <button 
              class="btn-download-certificate" 
              @click="downloadCertificate(investment.id)" 
              :disabled="downloadingCertificates[investment.id]"
              title="Zertifikat herunterladen"
            >
              <svg v-if="!downloadingCertificates[investment.id]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              <svg v-else class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
              {{ downloadingCertificates[investment.id] ? 'Lädt...' : 'PDF' }}
            </button>
          </div>
        </div>
      </div>

    </div>
    <!-- ENDE: Investor Dashboard -->

    <!-- Fallback für andere Rollen -->
    <div v-else class="dashboard-layout">
      <div class="dashboard-main">
        <div class="dashboard-section">
          <div class="section-header">
            <h3>Dashboard</h3>
            <p class="muted">Willkommen im Dashboard</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Pitch-Erstellung wurde in eine eigene Seite verschoben: /pitches/formular -->

    <!-- NEU: Modales Fenster zum Erstellen eines neuen Events -->
    <div v-if="showCreateEventModal" id="create-event-modal" class="modal-overlay" @click.self="showCreateEventModal = false">
      <div class="card modal-content">
        <h3>Neues Event erstellen</h3>
        <p class="muted">Fülle die Felder aus, um ein neues Event zu planen.</p>
        <form @submit.prevent="handleCreateEvent">
          <div class="input-group">
            <label for="eventName">Name des Events *</label>
            <input 
              id="eventName" 
              v-model="newEvent.name" 
              type="text" 
              placeholder="z.B. Tech Meetup Berlin" 
              :class="{ 'error': validationErrors.name }"
              required
            >
            <span v-if="validationErrors.name" class="error-text">{{ validationErrors.name }}</span>
          </div>
          <div class="grid-2 gap-12">
              <div class="input-group">
                <label for="eventDuration">Dauer (Minuten) *</label>
                <input 
                  id="eventDuration" 
                  v-model.number="newEvent.duration" 
                  type="number" 
                  min="1" 
                  max="480"
                  placeholder="z.B. 90" 
                  :class="{ 'error': validationErrors.duration }"
                  required
                >
                <span v-if="validationErrors.duration" class="error-text">{{ validationErrors.duration }}</span>
              </div>
              <div class="input-group">
                <label for="eventLocation">Ort/Platform *</label>
                <input 
                  id="eventLocation" 
                  v-model="newEvent.location" 
                  type="text" 
                  placeholder="z.B. MS Teams, Zoom" 
                  :class="{ 'error': validationErrors.location }"
                  required
                >
                <span v-if="validationErrors.location" class="error-text">{{ validationErrors.location }}</span>
              </div>
          </div>
          <div class="input-group">
            <label for="eventTopic">Thema *</label>
            <input 
              id="eventTopic" 
              v-model="newEvent.topic" 
              type="text" 
              placeholder="z.B. AI & Web3" 
              :class="{ 'error': validationErrors.topic }"
              required
            >
            <span v-if="validationErrors.topic" class="error-text">{{ validationErrors.topic }}</span>
          </div>
          <div class="input-group">
            <label for="eventDate">Datum und Uhrzeit *</label>
            <input 
              id="eventDate" 
              v-model="newEvent.date" 
              type="datetime-local" 
              :class="{ 'error': validationErrors.date }"
              required
            >
            <span v-if="validationErrors.date" class="error-text">{{ validationErrors.date }}</span>
          </div>
          <div class="input-group">
            <label for="eventHost">Host/Organisation</label>
            <input 
              id="eventHost" 
              v-model="newEvent.host" 
              type="text" 
              placeholder="z.B. HealthInvest (optional)"
            >
          </div>
          <div class="input-group">
            <label for="eventLink">Online Link (optional)</label>
            <input id="eventLink" v-model="newEvent.link" type="url" placeholder="https://teams.microsoft.com/...">
          </div>
          <div class="input-group">
            <label for="eventImage">🖼️ Event Bild (JPG/PNG, optional, max. 5MB)</label>
            <input 
              id="eventImage" 
              type="file" 
              accept="image/jpeg,image/png,image/jpg" 
              @change="handleEventImageChange($event)"
            >
            <small v-if="eventImageFile" class="muted block mt-4">
              Ausgewählt: {{ eventImageFile.name }}
            </small>
            <small v-if="existingEventImage" class="muted block mt-4">
              Aktuell: <a :href="existingEventImage" target="_blank" class="text-accent">Vorhandenes Bild anzeigen</a>
            </small>
            <div v-if="eventImagePreview" class="mt-12">
              <img :src="eventImagePreview" alt="Preview" style="max-width: 300px; max-height: 200px; border-radius: 8px; border: 2px solid var(--accent);">
            </div>
          </div>
          <div class="input-group">
            <label for="eventDesc">Beschreibung *</label>
            <div style="position: relative">
              <textarea 
                id="eventDesc" 
                v-model="newEvent.description" 
                rows="3" 
                placeholder="Panel: Regulierung & Markteintritt..."
                :class="{ 'error': validationErrors.description }"
                required
              ></textarea>
              <button 
                type="button" 
                class="ai-assist-btn" 
                @click="showAiModal = true"
                title="Mit KI verbessern"
              >
                ✨ KI-Assistent
              </button>
            </div>
            <span v-if="validationErrors.description" class="error-text">{{ validationErrors.description }}</span>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn ghost" @click="showCreateEventModal = false">Abbrechen</button>
            <button type="submit" class="btn primary">Event erstellen</button>
          </div>
        </form>
      </div>
    </div>

    <!-- NEU: Edit Event Modal -->
    <div v-if="showEditEventModal" class="modal-overlay" @click.self="showEditEventModal = false">
      <div class="card modal-content">
        <h3>Event bearbeiten</h3>
        <form @submit.prevent="handleUpdateEvent">
          <div class="input-group">
            <label>Name des Events *</label>
            <input v-model="editingEvent.name" type="text" required>
          </div>
          <div class="grid-2 gap-12">
              <div class="input-group">
                <label>Dauer (Minuten) *</label>
                <input v-model.number="editingEvent.duration" type="number" min="1" max="480" required>
              </div>
              <div class="input-group">
                <label>Ort/Platform *</label>
                <input v-model="editingEvent.location" type="text" required>
              </div>
          </div>
          <div class="input-group">
            <label>Thema *</label>
            <input v-model="editingEvent.topic" type="text" required>
          </div>
          <div class="input-group">
            <label>Datum und Uhrzeit *</label>
            <input v-model="editingEvent.date" type="datetime-local" required>
          </div>
          <div class="input-group">
            <label>Host/Organisation</label>
            <input v-model="editingEvent.host" type="text">
          </div>
          <div class="input-group">
            <label>Online Link</label>
            <input v-model="editingEvent.link" type="url">
          </div>
          <div class="input-group">
            <label for="editEventImage">🖼️ Event Bild (JPG/PNG, optional, max. 5MB)</label>
            <input 
              id="editEventImage" 
              type="file" 
              accept="image/jpeg,image/png,image/jpg" 
              @change="handleEditEventImageChange($event)"
            >
            <small v-if="editEventImageFile" class="muted block mt-4">
              Ausgewählt: {{ editEventImageFile.name }}
            </small>
            <small v-if="editingEvent.img && !editEventImageFile" class="muted block mt-4">
              Aktuell: <a :href="getImageUrl(editingEvent.img, editingEvent.name)" target="_blank" class="text-accent">Vorhandenes Bild anzeigen</a>
            </small>
            <div v-if="editEventImagePreview" class="mt-12">
              <img :src="editEventImagePreview" alt="Preview" style="max-width: 300px; max-height: 200px; border-radius: 8px; border: 2px solid var(--accent);">
            </div>
          </div>
          <div class="input-group">
            <label>Beschreibung *</label>
            <textarea v-model="editingEvent.description" rows="3" required></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn ghost" @click="showEditEventModal = false">Abbrechen</button>
            <button type="submit" class="btn primary">Speichern</button>
          </div>
        </form>
      </div>
    </div>

  </section>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const phases = ref(['Pre-Seed', 'Seed', 'Series A', 'Wachstum', 'Reife']);

const user = ref({ username: 'Startup-User', email: 'demo@startup.com', role: 'startup' }); // Default-Werte für Demo
const myPitches = ref([]); // Startet mit einer leeren Liste
const myEvents = ref([]); // NEU: Liste für Events
const savedPitches = ref([]); // NEU: Gespeicherte Pitches für Investoren
const myInvestments = ref([]); // Liste der Investments (für Testing)
const downloadingCertificates = ref({}); // Tracking für Download-Status
const showCreateModal = ref(false);
const showCreateEventModal = ref(false); // NEU: State für Event-Modal
const showAiModal = ref(false);
const showEditEventModal = ref(false); // State für Edit-Modal
const eventToDelete = ref(null); // Event das gelöscht werden soll
const editingEvent = ref(null); // Event das bearbeitet wird
const validationErrors = ref({}); // Validierungsfehler

const pitchToDelete = ref(null);

// Datenmodell für einen neuen Pitch
const newPitch = ref({
  id: null,
  title: '',
  sector: '',
  stage: '', 
  goal: '',
  equity: null,
  desc: '',
  img: 'https://placehold.co/600x400/22c55e/ffffff?text=Neu'
});

// Event form model
const newEvent = ref({
  id: null,
  name: '',
  duration: null,
  location: '',
  topic: '',
  date: '',
  host: '',
  link: '',
  description: '',
  img: null
});

const eventImageFile = ref(null);
const eventImagePreview = ref(null);
const existingEventImage = ref(null);

const editEventImageFile = ref(null);
const editEventImagePreview = ref(null);

// Investor KPI data - loaded dynamically from API
const investorKPIs = ref({
  totalInvested: 0,
  startupCount: 0,
  activeStartups: 0,
  watchlistCount: 0,
  newThisWeek: 0,
  avgInvestment: 0,
  portfolioGrowth: 0,
  roiForecast: 0,
  projectedReturn: 0,
  successRate: 0,
  successfulExits: 0,
  matchingSuggestions: [],
  recentActivity: []
});

// LocalStorage helpers: load/save lists so created items survive page reloads (Option A)
function savePitchesToLocalStorage() {
  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem('myPitches', JSON.stringify(myPitches.value));
    } catch (e) {
      console.warn('Failed to save myPitches to localStorage', e);
    }
  }
}

function saveEventsToLocalStorage() {
  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem('myEvents', JSON.stringify(myEvents.value));
    } catch (e) {
      console.warn('Failed to save myEvents to localStorage', e);
    }
  }
}

// Berechnet den Firmenwert automatisch
const calculatedValuation = computed(() => {
  const goal = Number(String(newPitch.value.goal).replace(/[^0-9]/g, ''));
  const equity = newPitch.value.equity;

  if (goal > 0 && equity > 0 && equity <= 100) {
    const valuation = (goal / equity) * 100;
    return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(valuation);
  }
  return null;
});

onMounted(async () => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (token) {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/users/me/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (res.ok) {
        const data = await res.json();
        user.value.username = data.username || '';
        user.value.email = data.email || '';
        user.value.role = data.profile?.role || data.role || 'startup';
      } else {
        console.error('Failed to load user data:', res.status);
        const errorText = await res.text();
        console.error('Error response:', errorText);
      }
    } catch (e) {
      console.error('Failed fetching /api/users/me/:', e);
    }
  } else {
    console.warn('No access token found - user may not be logged in');
  }

  // Load pitches from backend
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/pitches/?mine=true`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const backendPitches = await res.json();
        myPitches.value = backendPitches;
      } else {
        console.warn('Backend pitches request failed with status', res.status);
        loadPitchesFromLocalStorage();
      }
    } catch (e) {
      console.warn('Failed to fetch pitches from backend, falling back to localStorage', e);
      loadPitchesFromLocalStorage();
    }
  } else {
    loadPitchesFromLocalStorage();
  }

  // Load events from backend
  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/events/?mine=true`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const backendEvents = await res.json();
        myEvents.value = backendEvents;
      } else {
        console.warn('Backend events request failed with status', res.status);
        loadEventsFromLocalStorage();
      }
    } catch (e) {
      console.warn('Failed to fetch events from backend, falling back to localStorage', e);
      loadEventsFromLocalStorage();
    }
  } else {
    loadEventsFromLocalStorage();
  }
  
  // Load investor-specific data
  if (user.value.role === 'investor') {
    await loadSavedPitches();
    await loadInvestorKPIs();
    await loadInvestments();
  }
});

function loadPitchesFromLocalStorage() {
  try {
    if (typeof window !== 'undefined') {
      const savedPitches = localStorage.getItem('myPitches');
      if (savedPitches) {
        myPitches.value = JSON.parse(savedPitches);
      } else {
        myPitches.value = [];
      }
    } else {
      myPitches.value = [];
    }
  } catch (e) {
    console.warn('Error loading saved data from localStorage', e);
    myPitches.value = [];
  }
}

function loadEventsFromLocalStorage() {
  try {
    if (typeof window !== 'undefined') {
      const savedEvents = localStorage.getItem('myEvents');
      if (savedEvents) {
        myEvents.value = JSON.parse(savedEvents);
      } else {
        myEvents.value = [];
      }
    } else {
      myEvents.value = [];
    }
  } catch (e) {
    console.warn('Error loading events from localStorage', e);
    myEvents.value = [];
  }
}

// Datum-Formatierung: "Do, 09.10 · 14:00"
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

// Text kürzen mit "..." am Ende
function truncateText(text, maxLength) {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

// Helper function to get the correct image URL
function getImageUrl(imgPath, fallbackText = 'Image') {
  if (!imgPath) {
    return 'https://placehold.co/600x400/3b82f6/ffffff?text=' + encodeURIComponent(fallbackText);
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

// Format currency for investor dashboard
function formatCurrency(amount) {
  if (amount >= 1000000) {
    return (amount / 1000000).toFixed(1) + 'M€';
  } else if (amount >= 1000) {
    return (amount / 1000).toFixed(0) + 'k€';
  }
  return amount.toLocaleString('de-DE') + '€';
}

// Navigate to pitch detail page
function navigateToDetail(pitchId) {
  const router = useRouter();
  router.push(`/detail/${pitchId}`);
}

// Load saved pitches for investors
async function loadSavedPitches() {
  if (user.value.role !== 'investor') return;
  
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (!apiBase || !token) return;
  
  try {
    const res = await fetch(`${apiBase}/saved-pitches/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (res.ok) {
      savedPitches.value = await res.json();
    } else {
      console.warn('Failed to load saved pitches:', res.status);
    }
  } catch (e) {
    console.error('Error loading saved pitches:', e);
  }
}

// Load investor KPIs dynamically from API
async function loadInvestorKPIs() {
  if (user.value.role !== 'investor') return;
  
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (!apiBase || !token) return;
  
  try {
    const res = await fetch(`${apiBase}/investor/kpis/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (res.ok) {
      const data = await res.json();
      investorKPIs.value = data;
    } else {
      console.warn('Failed to load investor KPIs:', res.status);
    }
  } catch (e) {
    console.error('Error loading investor KPIs:', e);
  }
}

// Remove a saved pitch
async function removeSavedPitch(pitchId) {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (!apiBase || !token) return;
  
  if (!confirm('Möchten Sie diesen Pitch wirklich aus der Watchlist entfernen?')) return;
  
  try {
    const res = await fetch(`${apiBase}/saved-pitches/unsave_pitch/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ pitch_id: pitchId })
    });
    
    if (res.ok) {
      // Remove from local list
      savedPitches.value = savedPitches.value.filter(saved => saved.pitch.id !== pitchId);
      console.debug('Removed saved pitch:', pitchId);
    } else {
      console.warn('Failed to remove saved pitch:', res.status);
      alert('Fehler beim Entfernen des Pitches.');
    }
  } catch (e) {
    console.error('Error removing saved pitch:', e);
    alert('Fehler beim Entfernen des Pitches.');
  }
}

// Load investor investments
async function loadInvestments() {
  if (user.value.role !== 'investor') return;
  
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (!apiBase || !token) return;
  
  try {
    const res = await fetch(`${apiBase}/investments/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (res.ok) {
      myInvestments.value = await res.json();
    } else {
      console.warn('Failed to load investments:', res.status);
    }
  } catch (e) {
    console.error('Error loading investments:', e);
  }
}

// Remove investment (for testing)
async function removeInvestment(investmentId) {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (!apiBase || !token) return;
  
  if (!confirm('Investment wirklich löschen?')) return;
  
  try {
    const res = await fetch(`${apiBase}/investments/${investmentId}/`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (res.ok) {
      // Remove from local list
      myInvestments.value = myInvestments.value.filter(inv => inv.id !== investmentId);
      // Reload KPIs to update dashboard
      await loadInvestorKPIs();
      alert('Investment erfolgreich gelöscht!');
    } else {
      console.warn('Failed to delete investment:', res.status);
      alert('Fehler beim Löschen des Investments.');
    }
  } catch (e) {
    console.error('Error deleting investment:', e);
    alert('Fehler beim Entfernen des Pitches.');
  }
}

// Download certificate PDF for investment
async function downloadCertificate(investmentId) {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (!apiBase || !token) {
    alert('Nicht eingeloggt oder keine API-Konfiguration.');
    return;
  }
  
  // Set loading state
  downloadingCertificates.value = { ...downloadingCertificates.value, [investmentId]: true };
  
  try {
    const res = await fetch(`${apiBase}/investments/${investmentId}/certificate/`, {
      method: 'GET',
      headers: { 
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (res.ok) {
      // Get the PDF blob
      const blob = await res.blob();
      
      // Get filename from content-disposition header or create default
      const contentDisposition = res.headers.get('content-disposition');
      let filename = 'Investify_Zertifikat.pdf';
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      setTimeout(() => {
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
      }, 100);
      
    } else {
      const errorData = await res.json().catch(() => ({ error: 'Unbekannter Fehler' }));
      console.error('Failed to download certificate:', res.status, errorData);
      alert(`Fehler beim Download: ${errorData.error || 'Bitte versuchen Sie es später erneut.'}`);
    }
  } catch (e) {
    console.error('Error downloading certificate:', e);
    alert('Fehler beim Herunterladen des Zertifikats. Bitte versuchen Sie es später erneut.');
  } finally {
    // Remove loading state
    downloadingCertificates.value = { ...downloadingCertificates.value, [investmentId]: false };
  }
}

function handleEventImageChange(event) {
  const file = event.target.files[0];
  if (!file) {
    eventImageFile.value = null;
    eventImagePreview.value = null;
    return;
  }
  
  // Client-seitige Validierung
  if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
    alert('Bitte nur JPG/PNG Bilder hochladen.');
    event.target.value = '';
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    alert('Bild zu groß. Maximum: 5MB');
    event.target.value = '';
    return;
  }
  
  eventImageFile.value = file;
  
  // Preview erstellen
  const reader = new FileReader();
  reader.onload = (e) => {
    eventImagePreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
}

function handleEditEventImageChange(event) {
  const file = event.target.files[0];
  if (!file) {
    editEventImageFile.value = null;
    editEventImagePreview.value = null;
    return;
  }
  
  // Client-seitige Validierung
  if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
    alert('Bitte nur JPG/PNG Bilder hochladen.');
    event.target.value = '';
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    alert('Bild zu groß. Maximum: 5MB');
    event.target.value = '';
    return;
  }
  
  editEventImageFile.value = file;
  
  // Preview erstellen
  const reader = new FileReader();
  reader.onload = (e) => {
    editEventImagePreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
}

async function openCreateModal() {
  showCreateModal.value = true;
  await nextTick();
  const modalElement = document.getElementById('create-pitch-modal');
  if (modalElement) {
    modalElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

function handleCreatePitch() {
  const pitchToAdd = { 
    ...newPitch.value, 
    id: Date.now(),
    valuation: calculatedValuation.value // Fügt den berechneten Wert hinzu
  };

  myPitches.value.unshift(pitchToAdd);
  // Persist immediately so the pitch remains after reload
  savePitchesToLocalStorage();
  console.log('Neuer Pitch erstellt:', pitchToAdd);
  showCreateModal.value = false;

  newPitch.value = {
    id: null, title: '', sector: '', stage: '', goal: '', equity: null, desc: '', img: 'https://placehold.co/600x400/22c55e/ffffff?text=Neu'
  };
}

// NEU: Funktion zum Öffnen des Event-Modals
async function openCreateEventModal() {
  showCreateEventModal.value = true;
  validationErrors.value = {};
  await nextTick();
  const modalElement = document.getElementById('create-event-modal');
  if (modalElement) {
    modalElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

// Helper: convert an ISO datetime (possibly with timezone) to a string
// accepted by <input type="datetime-local"> ("YYYY-MM-DDTHH:MM").
function isoToDatetimeLocal(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (isNaN(d.getTime())) return '';
  const pad = (n) => String(n).padStart(2, '0');
  const yyyy = d.getFullYear();
  const MM = pad(d.getMonth() + 1);
  const dd = pad(d.getDate());
  const hh = pad(d.getHours());
  const mm = pad(d.getMinutes());
  return `${yyyy}-${MM}-${dd}T${hh}:${mm}`;
}

// Validation für Event-Formular
function validateEventForm() {
  validationErrors.value = {};
  let isValid = true;
  
  if (!newEvent.value.name || newEvent.value.name.trim().length < 3) {
    validationErrors.value.name = 'Event-Name muss mindestens 3 Zeichen haben.';
    isValid = false;
  }
  
  if (!newEvent.value.duration || newEvent.value.duration <= 0) {
    validationErrors.value.duration = 'Dauer muss größer als 0 sein.';
    isValid = false;
  } else if (newEvent.value.duration > 480) {
    validationErrors.value.duration = 'Event kann maximal 8 Stunden (480 Min) dauern.';
    isValid = false;
  }
  
  const eventDate = new Date(newEvent.value.date);
  const now = new Date();
  if (!newEvent.value.date) {
    validationErrors.value.date = 'Bitte wähle ein Datum aus.';
    isValid = false;
  } else if (eventDate < now) {
    validationErrors.value.date = 'Event-Datum muss in der Zukunft liegen.';
    isValid = false;
  }
  
  if (!newEvent.value.topic || newEvent.value.topic.trim().length === 0) {
    validationErrors.value.topic = 'Thema ist erforderlich.';
    isValid = false;
  }
  
  if (!newEvent.value.location || newEvent.value.location.trim().length === 0) {
    validationErrors.value.location = 'Ort/Platform ist erforderlich.';
    isValid = false;
  }
  
  if (!newEvent.value.description || newEvent.value.description.trim().length === 0) {
    validationErrors.value.description = 'Beschreibung ist erforderlich.';
    isValid = false;
  }
  
  return isValid;
}

// NEU: Funktion zum Erstellen eines Events (mit Backend)
async function handleCreateEvent() {
  if (!validateEventForm()) {
    return;
  }

  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  if (apiBase && token) {
    try {
      // FormData für File Upload verwenden
      const formData = new FormData();
      
      formData.append('name', newEvent.value.name);
      formData.append('topic', newEvent.value.topic);
      formData.append('location', newEvent.value.location);
      formData.append('duration', newEvent.value.duration);
      formData.append('date', newEvent.value.date ? new Date(newEvent.value.date).toISOString() : '');
      formData.append('link', newEvent.value.link || '');
      formData.append('description', newEvent.value.description);
      formData.append('host', newEvent.value.host || user.value.username);
      
      // Bild hinzufügen (nur wenn ausgewählt)
      if (eventImageFile.value) {
        formData.append('img', eventImageFile.value);
      }
      
      const res = await fetch(`${apiBase}/events/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
          // KEIN Content-Type - Browser setzt automatisch mit boundary
        },
        body: formData
      });
      
      if (res.ok) {
        const createdEvent = await res.json();
        myEvents.value.unshift(createdEvent);
        console.log('Event erfolgreich erstellt:', createdEvent);
        showCreateEventModal.value = false;
        // Reset form
        newEvent.value = {
          id: null, name: '', duration: null, location: '', topic: '', date: '', host: '', link: '', description: '', img: null
        };
        eventImageFile.value = null;
        eventImagePreview.value = null;
      } else {
        const errorData = await res.json();
        console.error('Fehler beim Erstellen:', errorData);
        alert('Fehler beim Erstellen: ' + JSON.stringify(errorData));
      }
    } catch (e) {
      console.error('Create event failed:', e);
      alert('Netzwerkfehler beim Erstellen des Events.');
    }
  } else {
    // Fallback: localStorage (kann keine Files speichern)
    const eventToAdd = { 
      name: newEvent.value.name,
      topic: newEvent.value.topic,
      location: newEvent.value.location,
      duration: newEvent.value.duration,
      date: newEvent.value.date ? new Date(newEvent.value.date).toISOString() : null,
      link: newEvent.value.link || '',
      description: newEvent.value.description,
      host: newEvent.value.host || user.value.username,
      id: Date.now() 
    };
    myEvents.value.unshift(eventToAdd);
    saveEventsToLocalStorage();
    showCreateEventModal.value = false;
    newEvent.value = {
      id: null, name: '', duration: null, location: '', topic: '', date: '', host: '', link: '', description: '', img: null
    };
    eventImageFile.value = null;
    eventImagePreview.value = null;
  }
}

// Event bearbeiten
function openEditEventModal(event) {
  // copy event and normalize date for datetime-local input
  editingEvent.value = { ...event, date: isoToDatetimeLocal(event.date) };
  editEventImageFile.value = null;
  editEventImagePreview.value = null;
  showEditEventModal.value = true;
}

async function handleUpdateEvent() {
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  if (apiBase && token) {
    try {
      // FormData für File Upload verwenden
      const formData = new FormData();
      
      formData.append('name', editingEvent.value.name);
      formData.append('topic', editingEvent.value.topic);
      formData.append('location', editingEvent.value.location);
      formData.append('duration', editingEvent.value.duration);
      formData.append('date', editingEvent.value.date ? new Date(editingEvent.value.date).toISOString() : '');
      formData.append('link', editingEvent.value.link || '');
      formData.append('description', editingEvent.value.description);
      formData.append('host', editingEvent.value.host || '');
      
      // Bild hinzufügen (nur wenn neues Bild ausgewählt)
      if (editEventImageFile.value) {
        formData.append('img', editEventImageFile.value);
      }
      
      const res = await fetch(`${apiBase}/events/${editingEvent.value.id}/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`
          // KEIN Content-Type - Browser setzt automatisch mit boundary
        },
        body: formData
      });
      
      if (res.ok) {
        const updated = await res.json();
        const idx = myEvents.value.findIndex(e => e.id === updated.id);
        if (idx !== -1) myEvents.value[idx] = updated;
        console.log('Event erfolgreich aktualisiert');
        showEditEventModal.value = false;
        editEventImageFile.value = null;
        editEventImagePreview.value = null;
      } else {
        const errorData = await res.json();
        console.error('Fehler beim Aktualisieren:', errorData);
        alert('Fehler: ' + JSON.stringify(errorData));
      }
    } catch (e) {
      console.error('Update failed:', e);
      alert('Netzwerkfehler beim Aktualisieren.');
    }
  }
}

// Event löschen
function confirmDeleteEvent(event) {
  eventToDelete.value = event;
}

function cancelDeleteEvent() {
  eventToDelete.value = null;
}

async function deleteEvent() {
  if (!eventToDelete.value) return;
  
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/events/${eventToDelete.value.id}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (res.ok || res.status === 204) {
        myEvents.value = myEvents.value.filter(e => e.id !== eventToDelete.value.id);
        console.log('Event erfolgreich gelöscht');
        eventToDelete.value = null;
      } else {
        console.error('Fehler beim Löschen:', res.status);
        alert('Event konnte nicht gelöscht werden. Bist du der Eigentümer?');
      }
    } catch (e) {
      console.error('Delete failed:', e);
      alert('Netzwerkfehler beim Löschen.');
    }
  } else {
    // Fallback: localStorage
    myEvents.value = myEvents.value.filter(e => e.id !== eventToDelete.value.id);
    if (typeof window !== 'undefined') {
      localStorage.setItem('myEvents', JSON.stringify(myEvents.value));
    }
    eventToDelete.value = null;
  }
}

// Pitch löschen
function confirmDeletePitch(pitch) {
  pitchToDelete.value = pitch;
}

function cancelDeletePitch() {
  pitchToDelete.value = null;
}

async function deletePitch() {
  if (!pitchToDelete.value) return;
  
  const config = useRuntimeConfig();
  const apiBase = config.public?.apiBase;
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (apiBase && token) {
    try {
      const res = await fetch(`${apiBase}/pitches/${pitchToDelete.value.id}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (res.ok || res.status === 204) {
        myPitches.value = myPitches.value.filter(p => p.id !== pitchToDelete.value.id);
        console.log('Pitch erfolgreich gelöscht');
        pitchToDelete.value = null;
      } else {
        console.error('Fehler beim Löschen:', res.status);
        alert('Pitch konnte nicht gelöscht werden. Bist du der Eigentümer?');
      }
    } catch (e) {
      console.error('Delete failed:', e);
      alert('Netzwerkfehler beim Löschen.');
    }
  }
}

function handleAiGenerated(description) {
  newEvent.value.description = description;
}
</script>

<style scoped>
/* Dashboard-spezifische Styles - Globale Styles sind in main.css */

/* Dashboard Layout */
.dashboard-header {
  margin-bottom: 32px;
}

.dashboard-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 24px;
  align-items: start;
}

.dashboard-main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.dashboard-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.section-header h3 {
  font-size: 1.25rem;
  margin-bottom: 4px;
}

.section-header p {
  font-size: 0.9rem;
}

/* Pitches Grid */
.pitches-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.pitch-card {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.pitch-card:hover {
  border-color: rgba(94, 234, 212, 0.2);
  transform: translateY(-2px);
}

.pitch-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.pitch-content {
  padding: 16px;
}

.pitch-header {
  margin-bottom: 12px;
}

.pitch-header h4 {
  font-size: 1.1rem;
  margin: 0 0 8px 0;
}

.pitch-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.pitch-desc {
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 12px;
}

.pitch-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.stat-item {
  padding: 10px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.pitch-documents {
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
  margin-bottom: 12px;
}

.doc-label {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--muted);
}

.doc-links {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.doc-link {
  padding: 6px 12px;
  background: rgba(94, 234, 212, 0.05);
  border: 1px solid rgba(94, 234, 212, 0.1);
  border-radius: 6px;
  font-size: 0.85rem;
  text-decoration: none;
  color: var(--accent);
  transition: all 0.2s ease;
}

.doc-link:hover {
  background: rgba(94, 234, 212, 0.1);
  border-color: rgba(94, 234, 212, 0.3);
}

.pitch-actions {
  display: flex;
  gap: 8px;
}

/* Events List */
.events-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.event-card {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.event-card:hover {
  border-color: rgba(96, 165, 250, 0.2);
  transform: translateY(-2px);
}

.event-image {
  width: 100%;
  height: 140px;
  object-fit: cover;
}

.event-content {
  padding: 16px;
}

.event-content h4 {
  font-size: 1.05rem;
  margin: 0 0 8px 0;
}

.event-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
  font-size: 0.875rem;
  color: var(--muted);
}

.event-desc {
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 12px;
}

.event-actions {
  display: flex;
  gap: 8px;
}

/* Sidebar */
.dashboard-sidebar {
  position: sticky;
  top: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.match-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.match-item:hover {
  background: rgba(255, 255, 255, 0.04);
}

.match-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #021;
}

.match-name {
  font-weight: 600;
  margin-bottom: 4px;
}

/* Stats Grid (für Investor) */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* Delete Confirmation Styling */
.delete-confirmation {
  margin-top: 12px;
  padding: 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  backdrop-filter: blur(8px);
}

.ai-assist-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 6px 12px;
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  border: none;
  border-radius: 6px;
  color: #021;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 4px;
  z-index: 10;
}

.ai-assist-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(94, 234, 212, 0.4);
}

/* Modal Overlay Override for Dashboard */
.modal-overlay {
  overflow-y: auto;
}

.modal-content {
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  margin: auto;
}

/* Investor Dashboard */
.investor-dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 20px;
}

.section-header-inline {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.link-with-icon {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--accent);
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 600;
  transition: all 0.2s;
}

.link-with-icon svg {
  width: 16px;
  height: 16px;
  transition: transform 0.2s;
}

.link-with-icon:hover {
  color: var(--accent-2);
}

.link-with-icon:hover svg {
  transform: translateX(4px);
}

/* KPI Section */
.kpi-section {
  animation: fadeInUp 0.5s ease-out;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.kpi-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(94, 234, 212, 0.05), rgba(59, 130, 246, 0.05));
  opacity: 0;
  transition: opacity 0.3s;
}

.kpi-card:hover {
  transform: translateY(-4px);
  border-color: rgba(94, 234, 212, 0.3);
  box-shadow: 0 8px 32px rgba(94, 234, 212, 0.15);
}

.kpi-card:hover::before {
  opacity: 1;
}

.kpi-icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

.primary-glow {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.2));
  box-shadow: 0 4px 24px rgba(59, 130, 246, 0.4);
}

.accent-glow {
  background: linear-gradient(135deg, rgba(94, 234, 212, 0.2), rgba(20, 184, 166, 0.2));
  box-shadow: 0 4px 24px rgba(94, 234, 212, 0.4);
}

.warning-glow {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(245, 158, 11, 0.2));
  box-shadow: 0 4px 24px rgba(251, 191, 36, 0.4);
}

.success-glow {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(22, 163, 74, 0.2));
  box-shadow: 0 4px 24px rgba(34, 197, 94, 0.4);
}

.kpi-icon {
  width: 32px;
  height: 32px;
  color: var(--accent);
}

.kpi-content {
  flex: 1;
  position: relative;
  z-index: 1;
}

.kpi-label {
  font-size: 0.875rem;
  color: var(--muted);
  margin-bottom: 8px;
  font-weight: 500;
}

.kpi-value {
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
  line-height: 1;
  margin-bottom: 8px;
}

.kpi-trend {
  font-size: 0.875rem;
  font-weight: 600;
  display: inline-block;
  padding: 4px 8px;
  border-radius: 6px;
}

.kpi-trend.positive {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.1);
}

.kpi-trend.neutral {
  color: var(--muted);
  background: rgba(255, 255, 255, 0.05);
}

/* Performance Section */
.performance-section {
  animation: fadeInUp 0.6s ease-out;
}

.performance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}

.metric-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s;
}

.metric-card:hover {
  border-color: rgba(94, 234, 212, 0.2);
  transform: translateY(-2px);
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.metric-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
}

.metric-icon {
  width: 20px;
  height: 20px;
  color: var(--accent);
}

.metric-change {
  font-size: 0.875rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 8px;
}

.metric-change.positive {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.1);
}

.metric-chart {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 80px;
  margin-bottom: 16px;
}

.empty-chart-message {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--muted);
  font-size: 0.875rem;
  font-style: italic;
}

.mini-bar {
  flex: 1;
  background: linear-gradient(180deg, var(--accent), var(--accent-2));
  border-radius: 4px 4px 0 0;
  transition: all 0.3s;
  opacity: 0.7;
}

.metric-card:hover .mini-bar {
  opacity: 1;
}

.metric-value-large {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 12px;
  text-align: center;
}

.metric-footer {
  font-size: 0.875rem;
  color: var(--muted);
  text-align: center;
}

/* Success Ring */
.success-ring {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 20px auto;
}

.success-ring svg {
  transform: rotate(-90deg);
  width: 100%;
  height: 100%;
}

.ring-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.1);
  stroke-width: 3.8;
}

.ring-progress {
  fill: none;
  stroke: var(--accent);
  stroke-width: 3.8;
  stroke-linecap: round;
  transition: stroke-dasharray 1s ease-out;
}

.ring-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--accent);
}

/* Matching Section */
.matching-section {
  animation: fadeInUp 0.7s ease-out;
}

.matching-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
}

.matching-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
}

.matching-card:hover {
  transform: translateY(-4px);
  border-color: rgba(94, 234, 212, 0.3);
  box-shadow: 0 12px 40px rgba(94, 234, 212, 0.2);
}

.matching-header {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.matching-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.matching-card:hover .matching-image {
  transform: scale(1.05);
}

.matching-score {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  padding: 8px 12px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 700;
  color: var(--accent);
}

.score-icon {
  width: 16px;
  height: 16px;
  color: #fbbf24;
}

.matching-content {
  padding: 20px;
}

.matching-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 12px;
}

.matching-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.meta-tag {
  font-size: 0.75rem;
  padding: 4px 10px;
  background: rgba(94, 234, 212, 0.1);
  color: var(--accent);
  border-radius: 12px;
  font-weight: 600;
}

.matching-desc {
  font-size: 0.9rem;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 16px;
}

.matching-stats {
  display: flex;
  gap: 16px;
  padding: 12px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 12px;
}

.stat-mini {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-mini-label {
  font-size: 0.75rem;
  color: var(--muted);
  font-weight: 500;
}

.stat-mini-value {
  font-size: 1rem;
  font-weight: 700;
  color: var(--accent);
}

.matching-reason {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  color: var(--accent-2);
  font-weight: 500;
}

.matching-reason svg {
  width: 14px;
  height: 14px;
}

/* Activity Section */
.activity-section {
  animation: fadeInUp 0.8s ease-out;
}

.activity-list {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  transition: all 0.2s;
}

.activity-item:hover {
  background: rgba(255, 255, 255, 0.04);
  transform: translateX(4px);
}

.activity-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-icon svg {
  width: 20px;
  height: 20px;
}

.activity-icon.investment {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.activity-icon.watchlist {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.activity-icon.message {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.activity-meta {
  font-size: 0.85rem;
  color: var(--muted);
}

.activity-amount {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--accent);
}

/* Saved Pitches Section */
.saved-pitches-section {
  animation: fadeInUp 0.75s ease-out;
}

.saved-pitches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.saved-pitch-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  position: relative;
}

.saved-pitch-card:hover {
  border-color: rgba(94, 234, 212, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.saved-pitch-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.saved-pitch-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  transition: transform 0.3s;
}

.saved-pitch-card:hover .saved-pitch-image {
  transform: scale(1.05);
}

.saved-pitch-content {
  padding: 20px;
}

.saved-pitch-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 12px;
}

.saved-pitch-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.meta-badge {
  font-size: 0.75rem;
  padding: 4px 10px;
  background: rgba(94, 234, 212, 0.1);
  color: var(--accent);
  border-radius: 12px;
  font-weight: 600;
}

.saved-pitch-desc {
  font-size: 0.9rem;
  color: var(--muted);
  line-height: 1.5;
  margin-bottom: 12px;
}

.saved-pitch-stats {
  display: flex;
  gap: 16px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.stat-small {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-small-label {
  font-size: 0.75rem;
  color: var(--muted);
  font-weight: 500;
}

.stat-small-value {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--accent);
}

.btn-remove-saved {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  background: rgba(239, 68, 68, 0.9);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s;
  z-index: 10;
}

.saved-pitch-card:hover .btn-remove-saved {
  opacity: 1;
}

.btn-remove-saved svg {
  width: 16px;
  height: 16px;
  color: white;
}

.btn-remove-saved:hover {
  background: rgba(220, 38, 38, 1);
  transform: scale(1.1);
}

/* Investments Section (Testing) */
.investments-section {
  animation: fadeInUp 0.6s ease-out 0.5s backwards;
}

.investments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.investment-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s;
}

.investment-card:hover {
  border-color: rgba(94, 234, 212, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(94, 234, 212, 0.1);
}

.investment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 12px;
}

.investment-header h4 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  color: white;
}

.investment-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
}

.investment-status.active {
  background: rgba(34, 197, 94, 0.2);
  color: #86efac;
}

.investment-status.exited {
  background: rgba(59, 130, 246, 0.2);
  color: #93c5fd;
}

.investment-status.failed {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
}

.investment-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
}

.detail-label {
  color: var(--muted);
}

.detail-value {
  font-weight: 600;
  color: white;
}

.detail-value.positive {
  color: #86efac;
}

.detail-value.negative {
  color: #fca5a5;
}

.btn-remove-investment {
  width: 100%;
  padding: 10px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #fca5a5;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-remove-investment svg {
  width: 16px;
  height: 16px;
}

.btn-remove-investment:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
  transform: translateY(-1px);
}

.badge-count {
  background: rgba(94, 234, 212, 0.2);
  color: var(--accent);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

/* Documents Section (NEW) */
.documents-section {
  animation: fadeInUp 0.6s ease-out 0.6s backwards;
}

.section-description {
  color: var(--muted);
  font-size: 0.95rem;
  margin-top: 8px;
  margin-bottom: 24px;
  line-height: 1.5;
}

.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.document-card {
  background: linear-gradient(135deg, rgba(30, 58, 95, 0.12) 0%, rgba(16, 185, 129, 0.08) 100%);
  border: 1px solid rgba(94, 234, 212, 0.15);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.document-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, var(--accent) 0%, rgba(94, 234, 212, 0.3) 100%);
}

.document-card:hover {
  border-color: rgba(94, 234, 212, 0.4);
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(94, 234, 212, 0.15);
  background: linear-gradient(135deg, rgba(30, 58, 95, 0.18) 0%, rgba(16, 185, 129, 0.12) 100%);
}

.document-icon {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, rgba(94, 234, 212, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

.document-icon svg {
  width: 28px;
  height: 28px;
}

.document-content {
  flex: 1;
  min-width: 0;
}

.document-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: white;
  margin: 0 0 4px 0;
  letter-spacing: 0.3px;
}

.document-startup {
  font-size: 0.9rem;
  color: var(--accent);
  margin: 0 0 12px 0;
  font-weight: 500;
}

.document-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 0.85rem;
  color: var(--muted);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.meta-item svg {
  width: 14px;
  height: 14px;
  opacity: 0.7;
}

.btn-download-certificate {
  flex-shrink: 0;
  padding: 12px 20px;
  background: linear-gradient(135deg, var(--accent) 0%, rgba(16, 185, 129, 0.8) 100%);
  border: none;
  border-radius: 8px;
  color: var(--bg);
  font-size: 0.9rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 90px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 12px rgba(94, 234, 212, 0.2);
}

.btn-download-certificate svg {
  width: 18px;
  height: 18px;
}

.btn-download-certificate:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(94, 234, 212, 1) 0%, var(--accent) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(94, 234, 212, 0.35);
}

.btn-download-certificate:active:not(:disabled) {
  transform: translateY(0);
}

.btn-download-certificate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-download-certificate .spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.empty-saved-state {
  text-align: center;
  padding: 48px 24px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

.empty-saved-state .empty-icon {
  width: 64px;
  height: 64px;
  color: var(--muted);
  margin: 0 auto 16px;
}

.empty-saved-state .empty-text {
  font-size: 1.1rem;
  color: var(--muted);
  margin-bottom: 20px;
}

/* Utility Helper Classes */
.block { display: block; }
.text-danger { color: #ef4444; }
.text-muted { color: #cbd5e1; font-size: 0.9rem; }
.text-accent { color: var(--accent); }

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Design */
@media (max-width: 1024px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .performance-grid {
    grid-template-columns: 1fr;
  }
  
  .matching-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .investor-dashboard {
    padding: 16px;
  }
  
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .kpi-card {
    padding: 20px;
  }
  
  .kpi-value {
    font-size: 1.75rem;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
}
</style>