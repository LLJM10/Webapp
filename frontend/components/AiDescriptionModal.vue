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
import '~/assets/components/AiDescriptionModal.css';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'pitch', // 'pitch' oder 'event'
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

// Zurücksetzen wenn Modal geöffnet/geschlossen wird
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
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    
    if (!token) {
      error.value = 'Bitte melde dich an, um die KI zu nutzen';
      isGenerating.value = false;
      return;
    }
    
    const response = await fetch(`${apiBase}/ai/generate-description/`, {
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
    
    const data = await response.json();
    
    if (response.ok) {
      generatedText.value = data.description;
    } else if (response.status === 401) {
      error.value = 'Deine Sitzung ist abgelaufen. Bitte melde dich erneut an.';
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
