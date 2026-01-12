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
// Sicherstellen, dass useRole aus dem Composables-File geladen wird
import { useRole } from '~/composables/useDemoData'; 

const currentRole = useRole(); // Holen des globalen States über das Composable

/**
 * Aktualisiert den globalen Zustand der Rolle.
 */
function setRole(role) {
  currentRole.value = role
}
</script>