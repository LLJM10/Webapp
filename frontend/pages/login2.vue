<template>
  <div class="auth-container" style="position:relative;overflow:hidden;">
    <!-- Animated Circular Text Background -->
    <div style="position:absolute;top:10%;left:50%;transform:translateX(-50%);z-index:0;pointer-events:none;">
      <Motion
        :animate="{ rotate: currentRotation, scale: getCurrentScale() }"
        :transition="{ rotate: { duration: 0 }, scale: { type: 'spring', damping: 20, stiffness: 300 } }"
        class="m-0 mx-auto rounded-full w-[200px] h-[200px] relative font-black text-white text-center cursor-pointer origin-center text-accent"
        @mouseenter="handleHoverStart"
        @mouseleave="handleHoverEnd"
      >
        <span
          v-for="(letter, i) in letters"
          :key="i"
          class="absolute inline-block inset-0 text-2xl transition-all duration-500 ease-[cubic-bezier(0,0,0,1)]"
          :style="getLetterStyle(i)"
        >
          {{ letter }}
        </span>
      </Motion>
    </div>
    <div class="card" style="position:relative;z-index:1;">
      <div class="brand">
        <div class="logo">iv</div>
        <h1 class="title">Login bei investify</h1>
      </div>
      <p class="subtitle">Bitte melde dich an, um fortzufahren.</p>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="username">Benutzername</label>
          <input id="username" v-model="username" type="text" placeholder="Dein Benutzername" />
        </div>
        <div class="input-group">
          <label for="password">Passwort</label>
          <input id="password" v-model="password" type="password" placeholder="Dein Passwort" />
        </div>
        <button type="submit" class="btn primary">Anmelden</button>
      </form>
      <p class="link-text">
        Noch kein Konto?
        <NuxtLink to="/registration">Jetzt registrieren</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watchEffect, onUnmounted } from 'vue';
import { Motion } from 'motion-v';

const username = ref('');
const password = ref('');
const errorMessage = ref('');

const handleLogin = async () => {
  errorMessage.value = '';
  try {
    const response = await fetch('http://127.0.0.1:8000/api/token/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value }),
    });
    if (!response.ok) throw new Error('Benutzername oder Passwort ist falsch.');
    const data = await response.json();
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
    }
    await navigateTo('/dashboard');
  } catch (error: any) {
    errorMessage.value = error.message || 'Ein unbekannter Fehler ist aufgetreten.';
  }
};

// CircularText Animation
const circularText = ref('INVESTIFY');
const spinDuration = ref(20);
const onHover = ref('speedUp');
const letters = computed(() => Array.from(circularText.value));
const isHovered = ref(false);
const currentRotation = ref(0);
const animationId = ref<number | null>(null);
const lastTime = ref(Date.now());
const rotationSpeed = ref(0);

const getCurrentSpeed = () => {
  if (isHovered.value && onHover.value === 'pause') return 0;
  const baseDuration = spinDuration.value;
  const baseSpeed = 360 / baseDuration;
  if (!isHovered.value) return baseSpeed;
  switch (onHover.value) {
    case 'slowDown': return baseSpeed / 2;
    case 'speedUp': return baseSpeed * 4;
    case 'goBonkers': return baseSpeed * 20;
    default: return baseSpeed;
  }
};
const getCurrentScale = () => (isHovered.value && onHover.value === 'goBonkers' ? 0.8 : 1);
const animate = () => {
  if (typeof window === 'undefined') return;
  const now = Date.now();
  const deltaTime = (now - lastTime.value) / 1000;
  lastTime.value = now;
  const targetSpeed = getCurrentSpeed();
  const speedDiff = targetSpeed - rotationSpeed.value;
  const smoothingFactor = Math.min(1, deltaTime * 5);
  rotationSpeed.value += speedDiff * smoothingFactor;
  currentRotation.value = (currentRotation.value + rotationSpeed.value * deltaTime) % 360;
  animationId.value = window.requestAnimationFrame(animate);
};
const startAnimation = () => {
  if (typeof window === 'undefined') return;
  if (animationId.value) window.cancelAnimationFrame(animationId.value);
  lastTime.value = Date.now();
  rotationSpeed.value = getCurrentSpeed();
  animate();
};
if (typeof window !== 'undefined') {
  watchEffect(() => { startAnimation(); });
  startAnimation();
  onUnmounted(() => { if (animationId.value) window.cancelAnimationFrame(animationId.value); });
}
const handleHoverStart = () => { isHovered.value = true; };
const handleHoverEnd = () => { isHovered.value = false; };
const getLetterStyle = (index: number) => {
  // Calculate angle for each letter, add currentRotation for animation
  const angle = ((360 / letters.value.length) * index + currentRotation.value) * Math.PI / 180;
  const radius = 80; // px, adjust for circle size
  const x = Math.cos(angle) * radius;
  const y = Math.sin(angle) * radius;
  return {
    position: 'absolute',
    left: '50%',
    top: '50%',
    transform: `translate(-50%, -50%) translate(${x}px, ${y}px) rotate(${angle * 180 / Math.PI + 90}deg)`,
    WebkitTransform: `translate(-50%, -50%) translate(${x}px, ${y}px) rotate(${angle * 180 / Math.PI + 90}deg)`
  };
};
</script>
