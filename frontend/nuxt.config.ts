// nuxt.config.ts
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  
  // Haupt-Stylesheet-Datei
  css: [
    '~/assets/main.css' 
  ],
  
  
  app: {
    head: {
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        //Link zur Inter Schriftart
        { 
          rel: 'stylesheet', 
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap' 
        }
      ]
    }
  },
  
  // Module
  modules: ["@pinia/nuxt"],

  // Laufzeitkonfiguration
  runtimeConfig: {
    public: {
      apiBase: "http://127.0.0.1:8000/api"
    }
  }
})
