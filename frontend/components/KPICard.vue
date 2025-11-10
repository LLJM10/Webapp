<template>
  <div class="kpi-card" ref="cardRef">
    <div class="kpi-value">
      <span v-if="prefix">{{ prefix }}</span>
      <span>{{ displayValue }}</span>
      <span v-if="suffix">{{ suffix }}</span>
    </div>
    <div class="kpi-label">{{ label }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  value: {
    type: Number,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  prefix: {
    type: String,
    default: ''
  },
  suffix: {
    type: String,
    default: ''
  },
  duration: {
    type: Number,
    default: 2000
  }
});

const displayValue = ref(0);
const cardRef = ref(null);
let hasAnimated = false;

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !hasAnimated) {
        animate();
        hasAnimated = true;
      }
    });
  }, { threshold: 0.1 });

  if (cardRef.value) {
    observer.observe(cardRef.value);
  }
});

function animate() {
  const steps = 60;
  const increment = props.value / steps;
  let current = 0;
  const stepDuration = props.duration / steps;

  const interval = setInterval(() => {
    current += increment;
    if (current >= props.value) {
      displayValue.value = props.value;
      clearInterval(interval);
    } else {
      displayValue.value = Math.round(current);
    }
  }, stepDuration);
}
</script>

<style scoped>
.kpi-card {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.02);
  border-radius: var(--radius);
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.2s ease;
}

.kpi-card:hover {
  transform: translateY(-4px);
}

.kpi-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--accent);
  margin-bottom: 0.5rem;
}

.kpi-label {
  color: var(--muted);
  font-size: 1rem;
}
</style>