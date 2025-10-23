<template>
  <div class="test-container">
    <h1>{{"Beispiel Event Seite"}}</h1>
  </div>
</template>

<script setup>

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