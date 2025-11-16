import { onBeforeUnmount, onMounted } from 'vue'

/**
 * Lightweight, SSR-safe reduced-motion detector that only touches the
 * MediaQueryList on the client to avoid serializing browser objects into the
 * payload (which can upset hydration in some runtimes).
 */
export const usePrefersReducedMotion = () => {
  const prefersReducedMotion = useState<boolean>('prefers-reduced-motion', () => false)

  let mediaQuery: MediaQueryList | null = null
  let handleChange: ((event: MediaQueryListEvent) => void) | null = null

  onMounted(() => {
    if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') return

    mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    prefersReducedMotion.value = mediaQuery.matches

    handleChange = (event: MediaQueryListEvent) => {
      prefersReducedMotion.value = event.matches
    }

    if (typeof mediaQuery.addEventListener === 'function') {
      mediaQuery.addEventListener('change', handleChange)
    } else {
      // @ts-expect-error - addListener is deprecated but used for older browsers
      mediaQuery.addListener(handleChange)
    }
  })

  onBeforeUnmount(() => {
    if (!mediaQuery || !handleChange) return

    if (typeof mediaQuery.removeEventListener === 'function') {
      mediaQuery.removeEventListener('change', handleChange)
    } else {
      // @ts-expect-error - removeListener is deprecated but used for older browsers
      mediaQuery.removeListener(handleChange)
    }
  })

  return prefersReducedMotion
}
