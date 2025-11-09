// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: [
    'vuetify/styles',
    '@mdi/font/css/materialdesignicons.css',
    '~/assets/css/base.css',
    '~/assets/css/main.css'
  ],
  modules: ['@pinia/nuxt'],
  pinia: {
    autoImports: ['defineStore', 'storeToRefs', 'acceptHMRUpdate']
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api'
    }
  },
  app: {
    head: {
      titleTemplate: '%s | ایندکسو',
      defaultLocale: 'fa',
      htmlAttrs: {
        lang: 'fa',
        dir: 'rtl'
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'پلتفرم چندفروشنده‌ای با تمرکز بر تجربه فارسی و سئوی قوی برای بازار ایران.'
        }
      ]
    }
  },
  build: {
    transpile: ['vuetify']
  },
  vite: {
    define: {
      'process.env.DEBUG': false
    },
    ssr: {
      noExternal: ['vuetify']
    }
  }
})
