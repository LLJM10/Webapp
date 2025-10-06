// nuxt.config.ts

export default defineNuxtConfig({
  // Feste Konfigurationen
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  
  // 1. GLOBAL CSS: Lädt die Haupt-Stylesheet-Datei
  css: [
    '~/assets/main.css' 
  ],
  
  // 2. APP KONFIGURATION: Hier wird der HTML <head> Tag konfiguriert
  app: {
    head: {
      link: [
        // Die <link rel="preconnect" ...> Tags
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        // Der Haupt-Link zur Inter Schriftart
        { 
          rel: 'stylesheet', 
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap' 
        }
      ]
    }
  },
  
  // Module
  modules: ["@pinia/nuxt"],

  // Runtime Config (für API-Basis-URL)
  runtimeConfig: {
    public: {
      apiBase: "http://127.0.0.1:8000/api"
    }
  }
})
