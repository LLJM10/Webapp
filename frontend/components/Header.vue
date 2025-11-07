<template>
<header>
<div class="brand">
<NuxtLink to="/" class="logo" style="text-decoration:none;color:inherit;display:flex;align-items:center;justify-content:center">iv</NuxtLink>
<div>
<div style="font-weight:800">investify</div>
<div style="font-size:12px;color:var(--muted);margin-top:2px" v-if="authStore.access">Marktplatz · Netzwerk · Events</div>
</div>
</div>
<div style="display:flex;align-items:center;gap:12px">
<!-- Navigation nur anzeigen wenn eingeloggt -->
<nav id="topnav" v-if="authStore.access">
<NuxtLink to="/">Start</NuxtLink>
<NuxtLink to="/market">Marktplatz</NuxtLink>
<NuxtLink to="/events">Events</NuxtLink>
<NuxtLink to="/network">Networking</NuxtLink>
<NuxtLink to="/dashboard">Dashboard</NuxtLink>
<NuxtLink to="/profile">Profil</NuxtLink>
</nav>

<!-- Login/Logout Button basierend auf Auth-Status -->
<template v-if="!authStore.access">
  <NuxtLink to="/login" class="btn ghost" style="margin-left:8px">
      Login
  </NuxtLink>
</template>
<template v-else>
  <button @click="logout" class="btn ghost" style="margin-left:8px">
      Logout
  </button>
</template>

</div>
</header>
</template>
<script setup>
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

const logout = () => {
  authStore.logout()
  navigateTo('/login')
}
</script>
 
<style scoped>
#topnav a[aria-current="page"],
#topnav .router-link-active,
#topnav .router-link-exact-active,
#topnav .nuxt-link-active,
#topnav .active {
    color: var(--accent);
    transition: color .12s ease;
}
</style>
