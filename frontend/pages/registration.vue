<template>
  <div class="page-auth-wrapper">
    <TextType text="Willkommen bei Investify — Registrierung" className="header-typetext" />

    <div class="auth-container">
      <div class="card">
      <div class="brand">
        <div class="logo">iv</div>
        <h1 class="title">Konto erstellen</h1>
      </div>
      <p class="subtitle">Werde Teil von investify.</p>

      <div v-if="successMessage" class="success-message">
        <div style="font-size:48px;margin-bottom:12px">📧</div>
        {{ successMessage }}
        <p style="margin-top:12px;font-size:0.875rem">
          Falls du keine E-Mail erhältst, überprüfe bitte deinen Spam-Ordner.
        </p>
      </div>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleRegister">

        <div class="input-group">
          <label for="reg-username">Benutzername</label>
          <input id="reg-username" v-model="username" type="text" placeholder="Wähle einen Benutzernamen" />
        </div>

        <div class="input-group">
          <label for="reg-email">Mail</label>
          <input id="reg-email" v-model="email" type="email" placeholder="Deine E-Mail-Adresse" />
        </div>

        <div class="input-group">
          <label for="reg-role">Rolle</label>
          <div style="display:flex;gap:12px;">
            <button
              type="button"
              :class="['btn', role === 'startup' ? 'primary' : 'ghost']"
              @click="role = 'startup'"
              style="flex:1"
            >
              StartUp
            </button>
            <button
              type="button"
              :class="['btn', role === 'investor' ? 'primary' : 'ghost']"
              @click="role = 'investor'"
              style="flex:1"
            >
              Investor
            </button>
          </div>
        </div>

        <div class="input-group">
          <label for="reg-password">Passwort</label>
          <input id="reg-password" v-model="password" type="password" placeholder="Dein sicheres Passwort" />
        </div>

        <div class="input-group">
          <label for="reg-password2">Passwort bestätigen</label>
          <input id="reg-password2" v-model="password2" type="password" placeholder="Passwort wiederholen" />
        </div>

        <button type="submit" class="btn primary">Konto erstellen</button>
      </form>
      
      <p class="link-text">
        Schon ein Konto? 
        <NuxtLink to="/login">Hier anmelden</NuxtLink>
      </p>
    </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import TextType from '~/components/TextType.vue';

const username = ref('');
const email = ref('');
const role = ref('startup');
const password = ref('');
const password2 = ref('');
const errorMessage = ref('');
const successMessage = ref('');

const handleRegister = async () => {
  errorMessage.value = '';
  successMessage.value = '';
  if (password.value !== password2.value) {
    errorMessage.value = 'Die Passwörter stimmen nicht überein.';
    return;
  }
  try {
    const response = await fetch('http://127.0.0.1:8000/api/users/users/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, email: email.value, password: password.value, role: role.value }),
    });
    const data = await response.json();
    if (!response.ok) {
      const errorText = Object.values(data).join(' ');
      throw new Error(errorText || 'Registrierung fehlgeschlagen.');
    }
    successMessage.value = 'Registrierung erfolgreich! Bitte überprüfe deine E-Mails für den Verifizierungslink.';
    // Formular leeren
    username.value = '';
    email.value = '';
    password.value = '';
    password2.value = '';
  } catch (error: any) {
    errorMessage.value = error.message || 'Ein unbekannter Fehler ist aufgetreten.';
  }
};
</script>

<style>
:root {
  --bg: #061022;
  --card: #0b1320;
  --muted: #9fb0c8;
  --accent: #5eead4;
  --accent-2: #60a5fa;
  --radius: 12px;
}

body {
  font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  background: linear-gradient(180deg, #020a14, #071126 65%);
  color: #eaf6fb;
  margin: 0;
}

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

.success-message {
  background-color: rgba(34, 197, 94, 0.1);
  color: #4ade80;
  padding: 0.75rem;
  border: 1px solid rgba(34, 197, 94, 0.2);
  border-radius: 10px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.header-typetext {
  display: block;
  text-align: center;
  font-size: 2.25rem;
  font-weight: 800;
  margin: 1rem 0 1.25rem;
  color: var(--accent);
}

.page-auth-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>

