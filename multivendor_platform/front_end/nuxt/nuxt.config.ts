// https://nuxt.com/docs/api/configuration/nuxt-config
import { fileURLToPath } from 'node:url'
import { fa } from 'vuetify/locale'

const projectRoot = fileURLToPath(new URL('./', import.meta.url))

export default defineNuxtConfig({
  compatibilityDate: '2025-11-14',
  // Disable devtools in production to reduce memory usage
  devtools: { enabled: process.env.NODE_ENV !== 'production' },
  ssr: true,
  css: [
    'vuetify/styles',
    '@mdi/font/css/materialdesignicons.css',
    '@/assets/css/base.css',
    '@/assets/css/main.css'
  ],
  modules: ['@pinia/nuxt', 'vuetify-nuxt-module', '@vite-pwa/nuxt'],
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
        rtl: { fa: true },
        messages: { fa }
      },
      theme: {
        defaultTheme: 'light',
        themes: {
          light: {
            dark: false,
            colors: {
              // Green Color Palette
              primary: '#4CAF50',           // green
              secondary: '#388E3C',         // green-darken-2
              accent: '#69F0AE',            // green-accent-2
              error: '#D32F2F',
              info: '#0277BD',
              success: '#2E7D32',
              warning: '#F57C00',
              background: '#FFFFFF',
              surface: '#FFFFFF',
              'on-primary': '#FFFFFF',
              'on-secondary': '#FFFFFF',
              'on-accent': '#FFFFFF',
              'on-error': '#FFFFFF',
              'on-success': '#FFFFFF',
              'on-background': '#212121',
              'on-surface': '#212121',
              // Additional green variants
              'green': '#4CAF50',
              'green-lighten-5': '#E8F5E9',
              'green-lighten-4': '#C8E6C9',
              'green-lighten-3': '#A5D6A7',
              'green-lighten-2': '#81C784',
              'green-lighten-1': '#BBC863',
              'green-darken-1': '#658C58',
              'green-darken-2': '#388E3C',
              'green-darken-3': '#2E7D32',
              'green-darken-4': '#31694E',
              'green-accent-1': '#B9F6CA',
              'green-accent-2': '#69F0AE',
              'green-accent-3': '#00E676',
              'green-accent-4': '#00C853'
            }
          },
          dark: {
            dark: true,
            colors: {
              // Green Color Palette for Dark Theme
              primary: '#81C784',           // green-lighten-2 (lighter for dark theme)
              secondary: '#A5D6A7',         // green-lighten-3
              accent: '#B9F6CA',            // green-accent-1
              error: '#EF5350',
              info: '#42A5F5',
              success: '#66BB6A',
              warning: '#FFA726',
              background: '#121212',
              surface: '#1E1E1E',
              'on-primary': '#FFFFFF',
              'on-secondary': '#FFFFFF',
              'on-accent': '#FFFFFF',
              'on-error': '#FFFFFF',
              'on-success': '#FFFFFF',
              'on-background': '#E1E1E1',
              'on-surface': '#E1E1E1',
              // Additional green variants
              'green': '#4CAF50',
              'green-lighten-5': '#E8F5E9',
              'green-lighten-4': '#C8E6C9',
              'green-lighten-3': '#A5D6A7',
              'green-lighten-2': '#81C784',
              'green-lighten-1': '#BBC863',
              'green-darken-1': '#658C58',
              'green-darken-2': '#388E3C',
              'green-darken-3': '#2E7D32',
              'green-darken-4': '#31694E',
              'green-accent-1': '#B9F6CA',
              'green-accent-2': '#69F0AE',
              'green-accent-3': '#00E676',
              'green-accent-4': '#00C853'
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
      apiBase: process.env.NUXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api',
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL ?? 'https://indexo.ir'
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
        },
        { name: 'theme-color', content: '#4CAF50' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'default' },
        { name: 'apple-mobile-web-app-title', content: 'ایندکسو' },
        { name: 'mobile-web-app-capable', content: 'yes' }
      ],
      link: [
        { rel: 'apple-touch-icon', href: '/icons/apple-touch-icon.png' },
        { rel: 'mask-icon', href: '/icons/safari-pinned-tab.svg', color: '#4CAF50' }
      ]
    }
  },
  build: {
    transpile: ['vuetify']
    // Source maps disabled in vite.build section below
  },
  vite: {
    define: {
      'process.env.DEBUG': false
    },
    ssr: {
      noExternal: ['vuetify']
    },
    build: {
      // Optimize build for low-memory environments
      // Reduce memory usage by limiting chunk size
      chunkSizeWarningLimit: 500,
      // Disable source maps to reduce memory usage
      sourcemap: false,
      // Use esbuild for minification (more memory efficient than terser)
      minify: 'esbuild',
      rollupOptions: {
        output: {
          manualChunks: undefined, // Let Vite handle chunking automatically
          // Limit chunk sizes to reduce memory usage
          chunkFileNames: 'chunks/[name]-[hash].js',
          entryFileNames: 'entry-[hash].js',
          assetFileNames: 'assets/[name]-[hash].[ext]'
        },
        // Reduce memory usage during tree-shaking
        treeshake: {
          preset: 'smallest'
        }
      }
    },
    optimizeDeps: {
      // Reduce memory usage during dependency optimization
      include: ['vuetify', 'vue', 'pinia'],
      // Disable esbuild optimization to save memory (slower but uses less RAM)
      esbuildOptions: {
        target: 'es2020'
      }
    },
    // Reduce memory usage during dev server (also affects build)
    server: {
      fs: {
        strict: true
      }
    }
  },
  experimental: {
    payloadExtraction: false,
    viewTransition: true
  },
  routeRules: {
    // Disable prefetching for non-critical routes
    '/admin/**': { prerender: false, index: false },
    '/api-test': { prerender: false, index: false },
    // Enable prefetching for likely next pages
    '/products/**': { prerender: false },
    '/blog/**': { prerender: false },
    '/suppliers/**': { prerender: false },
    // Machinery routes - client-side only, no SSR prefetch
    '/machinery/**': { prerender: false, ssr: true }
  },
  nitro: {
    compressPublicAssets: true,
    minify: true,
    // Reduce memory usage during Nitro build
    experimental: {
      wasm: false // Disable WASM to reduce memory usage
    },
    // Allow self-signed certificates for staging API calls
    // This is safe for staging environments with self-signed certs
    devServer: {
      watch: []
    }
  },
  features: {
    inlineStyles: false
  },
  pwa: {
    registerType: 'autoUpdate',
    workbox: {
      cacheId: 'mv-platform-v1',
      cleanupOutdatedCaches: true,
      clientsClaim: true,
      skipWaiting: true,
      navigateFallback: '/offline',
      navigateFallbackDenylist: [/^\/api/, /^\/admin/, /^\/_nuxt/],
      // Exclude HTML from cache to always fetch fresh shell
      globPatterns: ['**/*.{js,css,png,svg,ico,jpg,jpeg,woff,woff2}'],
      runtimeCaching: [
        {
          urlPattern: /^https:\/\/.*\.(?:png|jpg|jpeg|svg|gif|webp|ico)$/i,
          handler: 'CacheFirst',
          options: {
            cacheName: 'image-cache',
            expiration: {
              maxEntries: 100,
              maxAgeSeconds: 60 * 60 * 24 * 30 // 30 days
            },
            cacheableResponse: {
              statuses: [0, 200]
            }
          }
        },
        {
          urlPattern: /^https?:\/\/.*\/api\/.*/i,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            expiration: {
              maxEntries: 50,
              maxAgeSeconds: 60 * 5 // 5 minutes
            },
            networkTimeoutSeconds: 10,
            cacheableResponse: {
              statuses: [0, 200]
            }
          }
        },
        {
          urlPattern: /^https?:\/\/.*\/static\/.*/i,
          handler: 'CacheFirst',
          options: {
            cacheName: 'static-cache',
            expiration: {
              maxEntries: 200,
              maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
            }
          }
        },
        {
          urlPattern: /^https?:\/\/.*\/media\/.*/i,
          handler: 'CacheFirst',
          options: {
            cacheName: 'media-cache',
            expiration: {
              maxEntries: 100,
              maxAgeSeconds: 60 * 60 * 24 * 7 // 7 days
            }
          }
        }
      ]
    },
    client: {
      installPrompt: true,
      periodicSyncForUpdates: 20
    },
    devOptions: {
      enabled: false,
      type: 'module'
    },
    manifest: {
      name: 'ایندکسو',
      short_name: 'ایندکسو',
      description: 'پلتفرم چندفروشنده‌ای با تمرکز بر تجربه فارسی و سئوی قوی برای بازار ایران.',
      theme_color: '#4CAF50',
      background_color: '#FFFFFF',
      display: 'standalone',
      orientation: 'portrait-primary',
      scope: '/',
      start_url: '/',
      lang: 'fa',
      dir: 'rtl',
      icons: [
        {
          src: '/icons/pwa-192x192.png',
          sizes: '192x192',
          type: 'image/png',
          purpose: 'any maskable'
        },
        {
          src: '/icons/pwa-512x512.png',
          sizes: '512x512',
          type: 'image/png',
          purpose: 'any maskable'
        },
        {
          src: '/icons/apple-touch-icon.png',
          sizes: '180x180',
          type: 'image/png'
        }
      ]
    }
  }
})
