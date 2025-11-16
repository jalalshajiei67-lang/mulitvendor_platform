import { onBeforeUnmount, ref } from 'vue'

export const usePrefersReducedMotion = () => {
  const prefersReducedMotion = ref(false)

  if (typeof window !== 'undefined') {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    prefersReducedMotion.value = mediaQuery.matches

    const handleChange = (event: MediaQueryListEvent) => {
      prefersReducedMotion.value = event.matches
    }

    if (typeof mediaQuery.addEventListener === 'function') {
      mediaQuery.addEventListener('change', handleChange)
    } else {
      // @ts-expect-error - addListener is deprecated but used for older browsers
      mediaQuery.addListener(handleChange)
    }

    onBeforeUnmount(() => {
      if (typeof mediaQuery.removeEventListener === 'function') {
        mediaQuery.removeEventListener('change', handleChange)
      } else {
        // @ts-expect-error - removeListener is deprecated but used for older browsers
        mediaQuery.removeListener(handleChange)
      }
    })
  }

  return prefersReducedMotion
}
