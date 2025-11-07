<template>
  <div class="verify-container">
    <div class="card" style="max-width:500px;margin:100px auto;padding:32px;text-align:center">
      <div v-if="loading">
        <h2>E-Mail wird verifiziert...</h2>
        <p class="muted">Bitte warten...</p>
      </div>
      
      <div v-else-if="success">
        <div style="font-size:64px;margin-bottom:16px">✅</div>
        <h2>E-Mail erfolgreich verifiziert!</h2>
        <p class="muted" style="margin-top:12px">
          Deine E-Mail-Adresse wurde erfolgreich bestätigt. Du kannst dich jetzt anmelden.
        </p>
        <NuxtLink to="/login" class="btn primary" style="margin-top:24px">
          Zum Login
        </NuxtLink>
      </div>
      
      <div v-else-if="error">
        <div style="font-size:64px;margin-bottom:16px">❌</div>
        <h2>Verifizierung fehlgeschlagen</h2>
        <p class="muted" style="margin-top:12px">
          {{ errorMessage }}
        </p>
        <NuxtLink to="/registration" class="btn ghost" style="margin-top:24px">
          Zur Registrierung
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useRuntimeConfig } from '#app';

const route = useRoute();
const config = useRuntimeConfig();

const loading = ref(true);
const success = ref(false);
const error = ref(false);
const errorMessage = ref('');

onMounted(async () => {
  const token = route.query.token;
  
  console.log('=== E-Mail Verifizierung ===');
  console.log('Token aus URL:', token);
  
  if (!token) {
    loading.value = false;
    error.value = true;
    errorMessage.value = 'Kein Verifizierungs-Token gefunden.';
    return;
  }

  const apiBase = config.public?.apiBase;
  console.log('API Base:', apiBase);
  console.log('Request URL:', `${apiBase}/users/verify-email/`);
  
  try {
    const res = await fetch(`${apiBase}/users/verify-email/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token })
    });

    console.log('Response Status:', res.status);
    console.log('Response OK:', res.ok);
    
    const data = await res.json();
    console.log('Response Data:', data);

    if (res.ok) {
      loading.value = false;
      success.value = true;
    } else {
      loading.value = false;
      error.value = true;
      errorMessage.value = data.error || 'Verifizierung fehlgeschlagen.';
      console.error('Error message:', errorMessage.value);
    }
  } catch (e) {
    console.error('Verification error:', e);
    loading.value = false;
    error.value = true;
    errorMessage.value = 'Netzwerkfehler bei der Verifizierung.';
  }
});
</script>

<style scoped>
.verify-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
