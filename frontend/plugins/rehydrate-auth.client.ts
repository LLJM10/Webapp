import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(() => {
  if (typeof window === 'undefined') return
  try {
    const access = localStorage.getItem('access_token')
    const refresh = localStorage.getItem('refresh_token')
    const auth = useAuthStore()

    if (access || refresh) {
      auth.$patch({ access: access, refresh: refresh })
    }

    const username = localStorage.getItem('user_username')
    const email = localStorage.getItem('user_email')
    const role = localStorage.getItem('user_role')
    if (username || email || role) {
      auth.$patch({ user: { username, email, role } })
    }
  } catch (e) {
    // ignore storage errors
  }
})
