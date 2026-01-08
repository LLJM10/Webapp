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

</script>

<style>

</style>