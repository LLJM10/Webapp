import { defineStore } from "pinia"

type TokenResponse = {
  access: string
  refresh: string
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    access: null as string | null,
    refresh: null as string | null,
    user: null as any
  }),

  actions: {
    async login(username: string, password: string) {
      const config = useRuntimeConfig()
      const data = await $fetch<TokenResponse>(`${config.public.apiBase}/token/`, {
        method: "POST",
        body: { username, password }
      })

      this.access = data.access
      this.refresh = data.refresh

      // Beispiel für geschützte API
      const user = await $fetch<{ message: string }>(
        `${config.public.apiBase}/api/secret/`,
        { headers: { Authorization: `Bearer ${this.access}` } }
      )
      this.user = user
    },

    async logout() {
      this.access = null
      this.refresh = null
      this.user = null
    }
  }
})
