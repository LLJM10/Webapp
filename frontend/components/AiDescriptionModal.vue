<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>✨ KI-Assistent</h2>
        <button class="close-btn" @click="closeModal">×</button>
      </div>

      <div class="modal-body">
        <div class="form-group">
          <label>Stichworte / Thema</label>
          <textarea 
            v-model="keywords" 
            placeholder="z.B. MedTech, Diagnostik-App, AI-gestützte Früherkennung..."
            rows="3"
            :disabled="isGenerating"
          ></textarea>
          <p class="hint">Gib ein paar Stichworte ein, die dein {{ type === 'event' ? 'Event' : 'Startup' }} beschreiben</p>
        </div>

        <div class="form-group">
          <label>Ton / Stil</label>
          <div class="tone-buttons">
            <button 
              v-for="t in tones" 
              :key="t.value"
              :class="['tone-btn', { active: tone === t.value }]"
              @click="tone = t.value"
              :disabled="isGenerating"
            >
              {{ t.icon }} {{ t.label }}
            </button>
          </div>
        </div>

        <button 
          class="btn-generate" 
          @click="generateDescription"
          :disabled="!keywords.trim() || isGenerating"
        >
          <span v-if="isGenerating">
            <span class="spinner"></span> Generiere...
          </span>
          <span v-else>
            ✨ Beschreibung generieren
          </span>
        </button>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div v-if="generatedText" class="result-section">
          <label>Generierte Beschreibung</label>
          <div class="result-box">
            <p class="result-text">{{ generatedText }}</p>
          </div>
          <div class="result-actions">
            <button class="btn ghost" @click="regenerate">
              🔄 Neu generieren
            </button>
            <button class="btn primary" @click="useDescription">
              ✓ Übernehmen
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRuntimeConfig } from '#app';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'pitch', // 'pitch' or 'event'
    validator: (value) => ['pitch', 'event'].includes(value)
  }
});

const emit = defineEmits(['close', 'generated']);

const keywords = ref('');
const tone = ref('professional');
const generatedText = ref('');
const isGenerating = ref(false);
const error = ref('');

const tones = [
  { value: 'professional', label: 'Professionell', icon: '💼' },
  { value: 'creative', label: 'Kreativ', icon: '🎨' },
  { value: 'technical', label: 'Technisch', icon: '🔧' }
];

// Reset when modal opens/closes
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    error.value = '';
    generatedText.value = '';
  }
});

function closeModal() {
  emit('close');
}

async function generateDescription() {
  if (!keywords.value.trim()) return;
  
  isGenerating.value = true;
  error.value = '';
  generatedText.value = '';
  
  try {
    const config = useRuntimeConfig();
    const apiBase = config.public?.apiBase;
    let token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    
    if (!token) {
      error.value = 'Bitte melde dich an, um die KI zu nutzen';
      isGenerating.value = false;
      return;
    }
    
    let response = await fetch(`${apiBase}/ai/generate-description/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        type: props.type,
        keywords: keywords.value,
        tone: tone.value
      })
    });
    
    // Token expired? Try refresh
    if (response.status === 401) {
      const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null;
      if (refreshToken) {
        const refreshResponse = await fetch(`${apiBase}/token/refresh/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh: refreshToken })
        });
        
        if (refreshResponse.ok) {
          const refreshData = await refreshResponse.json();
          token = refreshData.access;
          if (typeof window !== 'undefined') {
            localStorage.setItem('access_token', token);
          }
          
          // Retry original request with new token
          response = await fetch(`${apiBase}/ai/generate-description/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
              type: props.type,
              keywords: keywords.value,
              tone: tone.value
            })
          });
        }
      }
    }
    
    const data = await response.json();
    
    if (response.ok) {
      generatedText.value = data.description;
    } else {
      error.value = data.error || data.detail || 'Fehler beim Generieren der Beschreibung';
    }
  } catch (err) {
    error.value = 'Netzwerkfehler. Bitte versuche es erneut.';
    console.error('AI generation error:', err);
  } finally {
    isGenerating.value = false;
  }
}

function regenerate() {
  generateDescription();
}

function useDescription() {
  emit('generated', generatedText.value);
  closeModal();
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.modal-content {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--accent);
}

.form-group textarea {
  width: 100%;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: white;
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
  transition: all 0.2s;
}

.form-group textarea:focus {
  outline: none;
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.08);
}

.form-group textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.hint {
  margin-top: 8px;
  font-size: 0.875rem;
  color: var(--muted);
}

.tone-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.tone-btn {
  flex: 1;
  min-width: 140px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.95rem;
}

.tone-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.tone-btn.active {
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  border-color: var(--accent);
  color: #021;
  font-weight: 600;
}

.tone-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-generate {
  width: 100%;
  padding: 16px;
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  border: none;
  border-radius: 8px;
  color: #021;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(94, 234, 212, 0.4);
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  border-top-color: #021;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  margin-top: 16px;
  padding: 12px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #f87171;
  font-size: 0.9rem;
}

.result-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.result-box {
  background: rgba(94, 234, 212, 0.05);
  border: 1px solid rgba(94, 234, 212, 0.2);
  border-radius: 12px;
  padding: 20px;
  margin-top: 8px;
  min-height: 120px;
}

.result-text {
  color: white;
  font-size: 1.05rem;
  line-height: 1.7;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.result-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.result-actions button {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.result-actions .btn.ghost {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.result-actions .btn.ghost:hover {
  background: rgba(255, 255, 255, 0.05);
}

.result-actions .btn.primary {
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  border: none;
  color: #021;
}

.result-actions .btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(94, 234, 212, 0.4);
}

@media (max-width: 640px) {
  .modal-content {
    max-height: 95vh;
  }
  
  .tone-buttons {
    flex-direction: column;
  }
  
  .tone-btn {
    min-width: 100%;
  }
  
  .result-actions {
    flex-direction: column;
  }
}
</style>
