<template>
  <div class="test-container">
    <h1>{{ headingText }}</h1>

    <button class="btn primary" @click="runTestScript">Test erneut ausführen</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 1. Eine reaktive Variable für den Text der Überschrift erstellen.
const headingText = ref('Warte auf das Skript...');

// 2. Die Test-Logik in eine Funktion packen.
function runTestScript() {

  // Ändert den Wert der reaktiven Variable. Vue aktualisiert das HTML automatisch.
  headingText.value = 'Skript wurde ausgeführt!';

  // Gibt eine Nachricht in der Entwicklerkonsole aus (F12 drücken).
  console.log('Dies ist eine Test-Nachricht für die Konsole aus der Vue-Komponente.');
}

// 3. Den 'onMounted' Hook verwenden, um das Skript automatisch auszuführen,
//    sobald die Komponente auf der Seite geladen und "eingehängt" ist.
//    Dies ist das Vue-Äquivalent zu 'DOMContentLoaded' in normalem JavaScript.
onMounted(() => {
  runTestScript();
});
</script>

<style scoped>
/* Etwas Styling, damit die Seite gut aussieht */
.test-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 40px;
}

h1 {
  color: var(--accent-2); /* Nutzt die Farben aus deiner main.css */
  margin-bottom: 24px;
}
</style>