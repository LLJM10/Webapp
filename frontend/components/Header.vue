<template>
<header>
<div class="brand">
<NuxtLink to="/" class="logo" style="text-decoration:none;color:inherit;display:flex;align-items:center;justify-content:center">iv</NuxtLink>
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


<NuxtLink to="/login" class="btn ghost" style="margin-left:8px">
    Login
</NuxtLink>

</div>
</header>
</template>
<script setup>

</script>
 