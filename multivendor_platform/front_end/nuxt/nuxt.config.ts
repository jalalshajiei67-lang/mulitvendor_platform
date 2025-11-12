// https://nuxt.com/docs/api/configuration/nuxt-config
import { fileURLToPath } from 'node:url'

const projectRoot = fileURLToPath(new URL('./', import.meta.url))

export default defineNuxtConfig({
  devtools: { enabled: true },
  ssr: true,
  css: [
    'vuetify/styles',
    '@mdi/font/css/materialdesignicons.css',
    '@/assets/css/base.css',
    '@/assets/css/main.css'
  ],
  modules: ['@pinia/nuxt', 'vuetify-nuxt-module'],
  pinia: {
    autoImports: ['defineStore', 'storeToRefs', 'acceptHMRUpdate']
  },
  vuetify: {
    moduleOptions: {
      /* module specific options */
    },
    vuetifyOptions: {
      ssr: true,
      defaults: {
        VBtn: {
          color: 'primary',
          rounded: 'lg'
        }
      },
      icons: {
        defaultSet: 'mdi'
      },
      locale: {
        locale: 'fa',
        fallback: 'fa',
        rtl: {
          fa: true
        }
      },
      theme: {
        defaultTheme: 'light',
        themes: {
          light: {
            dark: false,
            colors: {
              // Cyan Color Palette
              primary: '#00BCD4',           // cyan
              secondary: '#0097A7',         // cyan-darken-2
              accent: '#18FFFF',            // cyan-accent-2
              error: '#D32F2F',
              info: '#0277BD',
              success: '#2E7D32',
              warning: '#F57C00',
              background: '#FFFFFF',
              surface: '#FFFFFF',
              'on-primary': '#FFFFFF',
              'on-secondary': '#FFFFFF',
              'on-accent': '#212121',
              'on-error': '#FFFFFF',
              'on-success': '#FFFFFF',
              'on-background': '#212121',
              'on-surface': '#212121',
              // Additional cyan variants
              'cyan': '#00BCD4',
              'cyan-lighten-5': '#E0F7FA',
              'cyan-lighten-4': '#B2EBF2',
              'cyan-lighten-3': '#80DEEA',
              'cyan-lighten-2': '#4DD0E1',
              'cyan-lighten-1': '#26C6DA',
              'cyan-darken-1': '#00ACC1',
              'cyan-darken-2': '#0097A7',
              'cyan-darken-3': '#00838F',
              'cyan-darken-4': '#006064',
              'cyan-accent-1': '#84FFFF',
              'cyan-accent-2': '#18FFFF',
              'cyan-accent-3': '#00E5FF',
              'cyan-accent-4': '#00B8D4'
            }
          },
          dark: {
            dark: true,
            colors: {
              // Cyan Color Palette for Dark Theme
              primary: '#4DD0E1',           // cyan-lighten-2 (lighter for dark theme)
              secondary: '#80DEEA',         // cyan-lighten-3
              accent: '#84FFFF',            // cyan-accent-1
              error: '#EF5350',
              info: '#42A5F5',
              success: '#66BB6A',
              warning: '#FFA726',
              background: '#121212',
              surface: '#1E1E1E',
              'on-primary': '#212121',
              'on-secondary': '#212121',
              'on-accent': '#212121',
              'on-error': '#FFFFFF',
              'on-success': '#FFFFFF',
              'on-background': '#E1E1E1',
              'on-surface': '#E1E1E1',
              // Additional cyan variants
              'cyan': '#00BCD4',
              'cyan-lighten-5': '#E0F7FA',
              'cyan-lighten-4': '#B2EBF2',
              'cyan-lighten-3': '#80DEEA',
              'cyan-lighten-2': '#4DD0E1',
              'cyan-lighten-1': '#26C6DA',
              'cyan-darken-1': '#00ACC1',
              'cyan-darken-2': '#0097A7',
              'cyan-darken-3': '#00838F',
              'cyan-darken-4': '#006064',
              'cyan-accent-1': '#84FFFF',
              'cyan-accent-2': '#18FFFF',
              'cyan-accent-3': '#00E5FF',
              'cyan-accent-4': '#00B8D4'
            }
          }
        }
      }
    }
  },
  alias: {
    '@': projectRoot,
    '~': projectRoot
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
