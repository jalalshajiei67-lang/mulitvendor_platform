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
                    // Material Design 3 Color Scheme
                    primary: '#1976D2',       // Blue
                    secondary: '#4CAF50',     // Green
                    accent: '#FF9800',        // Orange
                    error: '#F44336',         // Red
                    info: '#2196F3',          // Light Blue
                    success: '#4CAF50',       // Green
                    warning: '#FFC107',       // Amber
                    background: '#FAFAFA',    // Light Gray
                    surface: '#FFFFFF',       // White
                    'on-primary': '#FFFFFF',
                    'on-secondary': '#FFFFFF',
                    'on-success': '#FFFFFF',
                    'on-error': '#FFFFFF',
                    'on-background': '#1C1B1F',
                    'on-surface': '#1C1B1F',
                },
            },
            dark: {
                dark: true,
                colors: {
                    primary: '#2196F3',
                    secondary: '#4CAF50',
                    accent: '#FF9800',
                    error: '#F44336',
                    info: '#2196F3',
                    success: '#4CAF50',
                    warning: '#FB8C00',
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

