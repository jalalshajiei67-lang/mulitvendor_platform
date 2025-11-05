// src/plugins/vuetify.js
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
    components,
    directives,

    // Enable RTL globally
    rtl: true,

    // Enable Material Design 3
    // Color scheme extracted from indexo.ir/departments/machinery
    theme: {
        defaultTheme: 'light',
        themes: {
            light: {
                dark: false,
                colors: {
                    // Industrial/Machinery Color Scheme (from indexo.ir)
                    primary: '#1565C0',       // Deep Blue - Primary brand color
                    secondary: '#FF6F00',     // Orange - Accent/CTA color
                    accent: '#FF6F00',        // Orange accent
                    error: '#D32F2F',         // Red
                    info: '#0277BD',          // Info blue
                    success: '#2E7D32',       // Green
                    warning: '#F57C00',       // Amber/Orange warning
                    background: '#F5F5F5',    // Light Gray background
                    surface: '#FFFFFF',       // White surface
                    'on-primary': '#FFFFFF',
                    'on-secondary': '#FFFFFF',
                    'on-success': '#FFFFFF',
                    'on-error': '#FFFFFF',
                    'on-background': '#212121',
                    'on-surface': '#212121',
                },
            },
            dark: {
                dark: true,
                colors: {
                    primary: '#42A5F5',
                    secondary: '#FF9800',
                    accent: '#FF9800',
                    error: '#EF5350',
                    info: '#42A5F5',
                    success: '#66BB6A',
                    warning: '#FFA726',
                    background: '#121212',
                    surface: '#1E1E1E',
                    'on-primary': '#FFFFFF',
                    'on-secondary': '#FFFFFF',
                    'on-success': '#FFFFFF',
                    'on-error': '#FFFFFF',
                    'on-background': '#E1E1E1',
                    'on-surface': '#E1E1E1',
                },
            },
        },
    },

    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi,
        },
    },

    // Default configuration for Material Design 3
    defaults: {
        VCard: {
            elevation: 2,
            rounded: 'lg',
        },
        VBtn: {
            rounded: 'lg',
            elevation: 2,
        },
        VTextField: {
            variant: 'outlined',
            density: 'comfortable',
        },
        VSelect: {
            variant: 'outlined',
            density: 'comfortable',
        },
        VTextarea: {
            variant: 'outlined',
            density: 'comfortable',
        },
        VChip: {
            rounded: 'lg',
        },
    },
})

export default vuetify

