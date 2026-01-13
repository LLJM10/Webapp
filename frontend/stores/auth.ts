import { defineStore } from "pinia"

type TokenResponse = {
  access: string
  refresh: string
}

// Pinia Store für Authentifizierung - verwaltung JWT Tokens und User-State
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

      const user = await $fetch<{ message: string }>(
        `${config.public.apiBase}/api/secret/`,
        { headers: { Authorization: `Bearer ${this.access}` } }
      )
      this.user = user
    },

    async logout() {
      // Tokens und User-Daten aus Store und LocalStorage löschen
      this.access = null
      this.refresh = null
      this.user = null
      if (typeof window !== 'undefined') {
        try {
          localStorage.removeItem('user_username');
          localStorage.removeItem('user_email');
          localStorage.removeItem('user_role');
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        } catch (e) {}
      }
    }
  }
})
