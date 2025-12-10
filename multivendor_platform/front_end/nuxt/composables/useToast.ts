import { nextTick, computed } from 'vue'

type ToastColor = 'success' | 'error' | 'warning' | 'info' | 'primary'

type ToastOptions = {
  message: string
  color?: ToastColor
  timeout?: number
}

/**
 * Lightweight global toast composable built on top of Vuetify snackbars.
 * Stores toast state in a Nuxt state so it can be triggered from any component.
 */
export const useToast = () => {
  const state = useState('global-toast', () => ({
    visible: false,
    message: '',
    color: 'info' as ToastColor,
    timeout: 4000
  }))

  const showToast = async (options: ToastOptions) => {
    state.value.visible = false
    state.value.message = options.message
    state.value.color = options.color ?? 'info'
    state.value.timeout = options.timeout ?? 4000

    // Wait for DOM update to ensure the snackbar can retrigger
    await nextTick()
    state.value.visible = true
  }

  const hideToast = () => {
    state.value.visible = false
  }

  return {
    toastState: computed(() => state.value),
    showToast,
    hideToast
  }
}

