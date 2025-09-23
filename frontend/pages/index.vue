<template>
  <!-- Haupt-Container für die Seite -->
  <div class="login-container">
    <!-- Das Formular selbst -->
    <div class="login-form">
      <h1 class="title">Login</h1>
      <p class="subtitle">Bitte melde dich an, um fortzufahren.</p>

      <!-- Fehlermeldung, die nur angezeigt wird, wenn 'errorMessage' einen Wert hat -->
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

      <!-- Eingabefeld für den Benutzernamen -->
      <div class="input-group">
        <label for="username">Benutzername</label>
        <input id="username" v-model="username" type="text" placeholder="Dein Benutzername" />
      </div>

      <!-- Eingabefeld für das Passwort -->
      <div class="input-group">
        <label for="password">Passwort</label>
        <input id="password" v-model="password" type="password" placeholder="Dein Passwort" />
      </div>

      <!-- Login-Button, der die 'handleLogin'-Funktion aufruft -->
      <button @click="handleLogin" class="login-button">Anmelden</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const username = ref('');
const password = ref('');
const errorMessage = ref('');

// Die 'handleLogin' Funktion ist der Kern der Logik.
// Sie wird 'async', damit wir auf die Antwort des Servers warten können.
const handleLogin = async () => {
  errorMessage.value = ''; // Fehlermeldung bei jedem Versuch zurücksetzen

  try {
    // SCHRITT 1: DATEN SENDEN
    // Wir senden die eingegebenen Daten per 'fetch' an den API-Endpunkt, den 'simple-jwt' bereitstellt.
    // Dieser Endpunkt ist speziell dafür gemacht, Benutzerdaten zu überprüfen.
    const response = await fetch('http://127.0.0.1:8000/api/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    // SCHRITT 2: ANTWORT AUSWERTEN
    // Das Django-Backend hat die Daten erhalten und mit der Datenbank abgeglichen.
    // Jetzt schickt es eine Antwort. Wir prüfen, ob diese Antwort erfolgreich war.
    if (!response.ok) {
      // Wenn die Antwort nicht 'ok' ist (z.B. Status 401 Unauthorized), bedeutet das,
      // der Benutzer wurde nicht in der Datenbank gefunden oder das Passwort war falsch.
      // Wir werfen einen Fehler, der im 'catch'-Block unten behandelt wird.
      throw new Error('Benutzername oder Passwort ist falsch.');
    }

    // SCHRITT 3: ERFOLG VERARBEITEN
    // Wenn der Code hier ankommt, war der Login erfolgreich!
    // Das Backend hat Tokens zurückgeschickt, die den Benutzer identifizieren.
    const data = await response.json();
    console.log('Login erfolgreich, Token erhalten:', data);

    // Hier würdest du den Benutzer z.B. auf eine andere Seite weiterleiten
    // und die erhaltenen Tokens speichern, um eingeloggt zu bleiben.
    alert('Login erfolgreich!');
    // Beispiel für eine Weiterleitung:
    // const router = useRouter();
    // router.push('/todos');


  } catch (error: any) {
    // SCHRITT 4: FEHLER BEHANDELN
    // Falls irgendwo im Prozess ein Fehler auftritt (falsche Daten, Server nicht erreichbar),
    // wird er hier gefangen und dem Benutzer eine klare Fehlermeldung angezeigt.
    console.error('Login-Fehler:', error);
    errorMessage.value = error.message || 'Ein unbekannter Fehler ist aufgetreten.';
  }
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

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 0.75rem;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  margin-bottom: 1rem;
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
  box-sizing: border-box;
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

