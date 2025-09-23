<template>
  <!-- Haupt-Container für die Seite -->
  <div class="login-container">
    <!-- Das Formular selbst -->
    <div class="login-form">
      <h1 class="title">Login</h1>
      <p class="subtitle">Bitte melde dich an, um fortzufahren.</p>

      <!-- Eingabefeld für den Benutzernamen -->
      <div class="input-group">
        <label for="username">Benutzername</label>
        <!-- v-model verknüpft dieses Feld mit der 'username'-Variable im Script -->
        <input id="username" v-model="username" type="text" placeholder="Dein Benutzername" />
      </div>

      <!-- Eingabefeld für das Passwort -->
      <div class="input-group">
        <label for="password">Passwort</label>
        <!-- v-model verknüpft dieses Feld mit der 'password'-Variable im Script -->
        <input id="password" v-model="password" type="password" placeholder="Dein Passwort" />
      </div>

      <!-- Login-Button, der die 'handleLogin'-Funktion aufruft -->
      <button @click="handleLogin" class="login-button">Anmelden</button>
    </div>
  </div>
</template>

<script setup lang="ts">
// Importiert 'ref', um reaktive Variablen zu erstellen
import { ref } from 'vue';

// Definiert die Variablen, die an die Eingabefelder gebunden sind.
// 'ref' sorgt dafür, dass die Seite auf Änderungen reagiert.
const username = ref('');
const password = ref('');

// Diese Funktion wird ausgeführt, wenn der Button geklickt wird.
const handleLogin = () => {
  // Für den Test geben wir die Daten in der Browser-Konsole aus.
  console.log('Login versucht mit:', {
    username: username.value,
    password: password.value,
  });

  // NÄCHSTER SCHRITT:
  // Hier würdest du den Code einfügen, um diese Daten an dein Django-Backend
  // zu senden, z.B. mit der 'fetch'-API.
  alert(`Login-Versuch mit Benutzer: ${username.value}`);
};
</script>

<style scoped>
/* Stellt sicher, dass der Container die volle Höhe hat und zentriert ist */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}

/* Das Styling für die Formular-Box */
.login-form {
  background: white;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
}

.input-group {
  text-align: left;
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.input-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /* Stellt sicher, dass Padding die Breite nicht beeinflusst */
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #0056b3;
}
</style>
