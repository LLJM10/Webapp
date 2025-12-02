export default defineNuxtPlugin(() => {
  // DEAKTIVIERT: Dieses Plugin löschte fälschlicherweise User-Daten bei jedem Reload
  // und führte dazu, dass User "ausgeloggt" erschienen, obwohl Tokens noch gültig waren
  
  // Wenn du User-Daten beim Logout löschen willst, sollte das nur in auth.ts logout() passieren
  // Nicht bei jedem Seitenaufruf!
  
  /* ALTE IMPLEMENTIERUNG (VERURSACHTE PROBLEM):
  if (typeof window !== 'undefined') {
    try {
      const keys = ['user_username', 'user_email', 'user_role'];
      const present = keys.filter(k => localStorage.getItem(k) !== null);
      keys.forEach(k => localStorage.removeItem(k));
      if (present.length > 0) {
        console.debug('clear-stale-user plugin removed keys:', present);
      }
    } catch (e) {}
  }
  */
});
