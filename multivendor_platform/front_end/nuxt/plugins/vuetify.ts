import 'vuetify/styles'

import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { fa } from 'vuetify/locale'

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    ssr: true,
    components,
    directives,
    defaults: {
      VBtn: {
        color: 'primary',
        rounded: 'lg'
      }
    },
    icons: {
      defaultSet: 'mdi',
      aliases,
      sets: { mdi }
    },
    locale: {
      locale: 'fa',
      fallback: 'fa',
      messages: { fa },
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
            primary: '#00c58e',
            secondary: '#006f52',
            accent: '#fbbc05',
            background: '#ffffff'
          }
        }
      }
    }
  })

  nuxtApp.vueApp.use(vuetify)
})

