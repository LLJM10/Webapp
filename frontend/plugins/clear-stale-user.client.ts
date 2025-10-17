export default defineNuxtPlugin(() => {
  if (typeof window !== 'undefined') {
    try {
      const keys = ['user_username', 'user_email', 'user_role'];
      // Remove stale user_* keys to avoid showing an unrelated account
      const present = keys.filter(k => localStorage.getItem(k) !== null);
      keys.forEach(k => localStorage.removeItem(k));
      // Log if any of those keys were present (helpful for debugging)
      if (present.length > 0) {
        console.debug('clear-stale-user plugin removed keys:', present);
      }
    } catch (e) {
      // ignore any storage errors
    }
  }
});
