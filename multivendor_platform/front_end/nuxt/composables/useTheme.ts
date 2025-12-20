import { useTheme as useVuetifyTheme } from 'vuetify'

/**
 * Theme management composable
 * Provides theme switching functionality with localStorage persistence
 * Named useAppTheme to avoid conflict with Vuetify's useTheme
 */
export const useAppTheme = () => {
  // Vuetify theme composable - must be called unconditionally
  const theme = useVuetifyTheme()
  const STORAGE_KEY = 'vuetify-theme'

  // Initialize theme from localStorage or default to light
  const initializeTheme = () => {
    if (process.client) {
      const savedTheme = localStorage.getItem(STORAGE_KEY)
      if (savedTheme === 'dark' || savedTheme === 'light') {
        theme.global.name.value = savedTheme
      } else {
        theme.global.name.value = 'light'
        localStorage.setItem(STORAGE_KEY, 'light')
      }
    }
  }

  // Toggle between light and dark themes
  const toggleTheme = () => {
    const newTheme = theme.global.name.value === 'light' ? 'dark' : 'light'
    theme.global.name.value = newTheme
    
    if (process.client) {
      localStorage.setItem(STORAGE_KEY, newTheme)
    }
  }

  // Set theme explicitly
  const setTheme = (themeName: 'light' | 'dark') => {
    theme.global.name.value = themeName
    
    if (process.client) {
      localStorage.setItem(STORAGE_KEY, themeName)
    }
  }

  // Check if current theme is dark
  const isDark = computed(() => theme.global.name.value === 'dark')

  // Get current theme name
  const currentTheme = computed(() => theme.global.name.value)

  return {
    isDark,
    currentTheme,
    toggleTheme,
    setTheme,
    initializeTheme
  }
}

