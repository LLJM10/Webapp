<template>
  <div>
    <h1>Nuxt ↔ Django Test</h1>
    <pre>{{ data }}</pre>
    <pre>{{ error }}</pre>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()
const { data, error } = await useFetch("/hello/", {
  baseURL: config.public.apiBase,
})
</script>
