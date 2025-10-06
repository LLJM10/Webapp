<template>
<div class="role-toggle" title="Rolle wählen" style="margin-left:16px">
<div class="muted" style="font-size:13px">Ansicht:</div>
<button
     :class="['role-btn', { 'active': currentRole === 'startup' }]"
     @click="setRole('startup')"
>
     Startup
</button>
<button
     :class="['role-btn', { 'active': currentRole === 'investor' }]"
     @click="setRole('investor')"
>
     Investor
</button>
</div>
</template>
<script setup>
// Globaler State für die Rolle (wird bei Nuxt 3 in einem composable oder Store ausgelagert)
// Für dieses Mockup simulieren wir den State wie folgt:
const currentRole = useState('currentRole', () => 'startup') // 'startup' oder 'investor'
function setRole(role) {
 currentRole.value = role
 // Hinweis: In einem echten Nuxt-Projekt würden wir hier einen Store-Action auslösen
}
</script>