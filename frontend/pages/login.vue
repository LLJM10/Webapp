<template>
  <div class="auth-container">
    <div class="card">
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
import { ref } from 'vue';

const username = ref('');
const password = ref('');
const errorMessage = ref('');

const handleLogin = async () => {
  errorMessage.value = '';
  try {
    const response = await fetch('http://127.0.0.1:8000/api/token/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });
    if (!response.ok) throw new Error('Benutzername oder Passwort ist falsch.');
    const data = await response.json();
    if (typeof window !== 'undefined') {
      // Nur Tokens im localStorage speichern (sicherer)
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      // Optional: schnelle Validierung des Tokens durch Abruf des eigenen Profils
      try {
        const profileRes = await fetch('http://127.0.0.1:8000/users/me/', {
          headers: { 'Authorization': `Bearer ${data.access}` }
        });
        if (profileRes.ok) {
          // Wir holen die Userdaten nur zur Validierung, speichern sie aber nicht in localStorage
          const profileData = await profileRes.json();
          console.debug('Logged in user:', profileData);
        }
      } catch (e) {
        // ignore
      }
    }
    await navigateTo('/dashboard'); // Redirect to a protected page
  } catch (error: any) {
    errorMessage.value = error.message || 'Ein unbekannter Fehler ist aufgetreten.';
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
}

.card {
  background: var(--card);
  padding: 2.5rem;
  border-radius: var(--radius);
  border: 1px solid rgba(255, 255, 255, 0.02);
  width: 100%;
  max-width: 420px;
  text-align: center;
}

.brand {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.logo {
  width: 46px;
  height: 46px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 1.2rem;
  color: #021;
}

.title {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0;
}

.subtitle {
  color: var(--muted);
  margin-bottom: 1.5rem;
}

.input-group {
  text-align: left;
  margin-bottom: 1.25rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--muted);
}

.input-group input {
  width: 100%;
  padding: 0.8rem 1rem;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.04);
  color: #fff;
  font-size: 1rem;
  box-sizing: border-box;
}

.input-group input:focus {
  outline: none;
  border-color: var(--accent);
}

.btn {
  width: 100%;
  padding: 0.8rem 1rem;
  border-radius: var(--radius);
  border: 0;
  font-weight: 800;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.14s ease;
}

.btn:hover {
  transform: translateY(-3px);
}

.btn.primary {
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  color: #042;
}

.link-text {
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: var(--muted);
}

.link-text a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 700;
}

.error-message {
  background-color: rgba(239, 68, 68, 0.1);
  color: #f87171;
  padding: 0.75rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 10px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}
</style>

