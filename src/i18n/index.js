// src/i18n/index.js
import { createI18n } from 'vue-i18n'
import fa from './locales/fa'

const i18n = createI18n({
    legacy: false, // Use Composition API mode
    locale: 'fa', // Set Persian as default language
    fallbackLocale: 'fa',
    messages: {
        fa
    },
    globalInjection: true // Enable $t() globally
})

export default i18n


