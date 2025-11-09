import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [
    vue(),
    // Only use devtools in development
    mode !== 'production' && vueDevTools(),
  ].filter(Boolean),
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  // Optimize build and prevent corruption issues
  build: {
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
    chunkSizeWarningLimit: 2000,
    sourcemap: false,
  },
  // Only configure dev server in development mode
  ...(mode !== 'production' && {
    server: {
      host: '0.0.0.0',
      port: 5173,
      strictPort: false,
      hmr: {
        overlay: true,
      },
      watch: {
        usePolling: false,
        interval: 100,
      },
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          secure: false,
        },
        '/media': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        },
        '/admin': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        }
      }
    }
  }),
}))
