<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Login</h1>

    <input
      v-model="username"
      type="text"
      placeholder="Username"
      class="border p-2 w-full mb-2"
    />
    <input
      v-model="password"
      type="password"
      placeholder="Passwort"
      class="border p-2 w-full mb-2"
    />

    <button
      @click="doLogin"
      class="bg-blue-600 text-white px-4 py-2 rounded"
    >
      Login
    </button>

    <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
    <p v-if="auth.access" class="text-green-600 mt-2">
      ✅ Eingeloggt! Access Token vorhanden.
    </p>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "~/stores/auth"

const auth = useAuthStore()
const username = ref("")
const password = ref("")
const error = ref("")

async function doLogin() {
  try {
    error.value = ""
    await auth.login(username.value, password.value)
  } catch (e: any) {
    error.value = e.message
  }
}
</script>
