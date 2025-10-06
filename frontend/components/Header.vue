<template>
<header>
<div class="brand">
<div class="logo">iv</div>
<div>
<div style="font-weight:800">investify</div>
<div style="font-size:12px;color:var(--muted);margin-top:2px">Marktplatz · Netzwerk · Events</div>
</div>
</div>
<div style="display:flex;align-items:center;gap:12px">
<nav id="topnav">
<NuxtLink to="/">Start</NuxtLink>
<NuxtLink to="/market">Marktplatz</NuxtLink>
<NuxtLink to="/events">Events</NuxtLink>
<NuxtLink to="/network">Networking</NuxtLink>
<NuxtLink to="/dashboard">Dashboard</NuxtLink>
<NuxtLink to="/profile">Profil</NuxtLink>
</nav>
<RoleToggle />
</div>
</header>
</template>
<script setup>

// Kein spezielles Script hier, da die Logik in RoleToggle ist
</script>
 