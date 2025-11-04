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
                    // Brand Colors
                    primary: '#FFE512',        // Primary Brand - Yellow
                    secondary: '#2A2A72',      // Secondary Color - Dark Blue
                    accent: '#E53E3E',         // Accent Color - Red
                    error: '#E53E3E',          // Error - Same as accent
                    info: '#2A2A72',           // Info - Same as secondary
                    success: '#38A169',        // Success Color - Green
                    warning: '#FFE512',        // Warning - Same as primary
                    background: '#F5F5F7',     // Light Neutral - Background
                    surface: '#FFFFFF',        // White - Surface
                    'on-primary': '#1A1A1A',   // Dark text on primary
                    'on-secondary': '#FFFFFF', // White text on secondary
                    'on-accent': '#FFFFFF',    // White text on accent
                    'on-success': '#FFFFFF',   // White text on success
                    'on-error': '#FFFFFF',     // White text on error
                    'on-background': '#1A1A1A', // Dark Neutral - Text on background
                    'on-surface': '#1A1A1A',   // Dark Neutral - Text on surface
                },
            },
            dark: {
                dark: true,
                colors: {
                    // Dark Theme Brand Colors
                    primary: '#FFE512',        // Primary Brand - Yellow
                    secondary: '#2A2A72',      // Secondary Color - Dark Blue
                    accent: '#E53E3E',         // Accent Color - Red
                    error: '#E53E3E',          // Error - Same as accent
                    info: '#2A2A72',           // Info - Same as secondary
                    success: '#38A169',        // Success Color - Green
                    warning: '#FFE512',        // Warning - Same as primary
                    background: '#1A1A1A',     // Dark Neutral - Background
                    surface: '#2A2A2A',        // Slightly lighter dark for surface
                    'on-primary': '#1A1A1A',   // Dark text on primary
                    'on-secondary': '#FFFFFF', // White text on secondary
                    'on-accent': '#FFFFFF',    // White text on accent
                    'on-success': '#FFFFFF',   // White text on success
                    'on-error': '#FFFFFF',     // White text on error
                    'on-background': '#F5F5F7', // Light Neutral - Text on dark background
                    'on-surface': '#F5F5F7',   // Light Neutral - Text on dark surface
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

