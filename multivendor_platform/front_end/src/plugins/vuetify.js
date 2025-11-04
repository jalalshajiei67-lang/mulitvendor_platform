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
    theme: {
        defaultTheme: 'light',
        themes: {
            light: {
                dark: false,
                colors: {
                    // Custom Brand Color Scheme
                    primary: '#102E50',       // Custom Primary
                    secondary: '#2A2A72',     // Custom Secondary
                    accent: '#E53E3E',        // Custom Accent (used for error/warning)
                    error: '#E53E3E',         // Custom Error (same as accent)
                    info: '#2A2A72',          // Same as secondary
                    success: '#38A169',       // Custom Success
                    warning: '#E53E3E',       // Same as error
                    background: '#F5F5F7',    // Custom Light Neutral
                    surface: '#FFFFFF',       // White
                    'on-primary': '#FFFFFF',   // White text on primary
                    'on-secondary': '#FFFFFF', // White text on secondary
                    'on-success': '#FFFFFF',   // White text on success
                    'on-error': '#FFFFFF',     // White text on error
                    'on-background': '#1A1A1A', // Dark text on light background
                    'on-surface': '#1A1A1A',    // Dark text on light surface
                },
            },
            dark: {
                dark: true,
                colors: {
                    primary: '#102E50',       // Same primary for dark theme
                    secondary: '#2A2A72',     // Same secondary for dark theme
                    accent: '#E53E3E',        // Same accent for dark theme
                    error: '#E53E3E',         // Same error for dark theme
                    info: '#2A2A72',          // Same info for dark theme
                    success: '#38A169',       // Same success for dark theme
                    warning: '#E53E3E',       // Same warning for dark theme
                    background: '#1A1A1A',    // Custom Dark Neutral
                    surface: '#2A2A2A',       // Slightly lighter than background
                    'on-primary': '#FFFFFF',   // White text on primary
                    'on-secondary': '#FFFFFF', // White text on secondary
                    'on-success': '#FFFFFF',   // White text on success
                    'on-error': '#FFFFFF',     // White text on error
                    'on-background': '#FFFFFF', // Light text on dark background
                    'on-surface': '#FFFFFF',    // Light text on dark surface
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

