<template>
  <div class="feature">
    <strong>{{ title }}</strong>
    <p class="muted" style="margin-top:6px;font-size:14px">{{ desc }}</p>
  </div>
</template>

<script setup>
// Props definieren, um Titel und Beschreibung von der übergeordneten Komponente zu erhalten
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  desc: {
    type: String,
    required: true
  }
});
</script>