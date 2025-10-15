<template>
  <div>
    <Header /> 
    <main class="container">
      <NuxtPage />
    </main>
    <footer style="text-align:center;padding:22px;color:var(--muted);border-top:1px solid rgba(255,255,255,0.02)">
      
      © investify — Demo 2025 · 
      <NuxtLink to="/impressum">Impressum</NuxtLink> · 
      <NuxtLink to="/datenschutz">Datenschutz</NuxtLink>

    </footer>
    <div id="toast-container"></div>
  </div>
</template>

<script setup>
// Nuxt 3 Composition API Setup Script
// Kein Javascript nötig, da Header und Seiten die Logik übernehmen
</script>

<style>
/* Die globalen styles/main.css werden via nuxt.config.ts eingebunden */
</style>