import { computed, onScopeDispose, ref, watch } from 'vue'
import { usePreferredReducedMotion } from '@vueuse/core'

export type ScrollGalleryItem = {
  el: HTMLElement
  index: number
}

export const useScrollActivatedGallery = () => {
  const activeIndex = ref(0)
  const isPaused = ref(false)
  const prefersReducedMotion = usePreferredReducedMotion()

  let observer: IntersectionObserver | null = null
  let trackedElements: HTMLElement[] = []
  const visibilityMap = new Map<HTMLElement, number>()

  const isAutoActive = computed(() => !isPaused.value && !prefersReducedMotion.value)

  const cleanupObserver = () => {
    if (observer) {
      observer.disconnect()
      observer = null
    }
    visibilityMap.clear()
  }

  const updateActiveIndex = () => {
    if (!trackedElements.length || !isAutoActive.value) return

    const ranked = trackedElements
      .map((el, index) => ({
        index,
        ratio: visibilityMap.get(el) ?? 0
      }))
      .sort((a, b) => b.ratio - a.ratio)

    if (ranked[0] && ranked[0].ratio > 0) {
      activeIndex.value = ranked[0].index
    }
  }

  const handleIntersections: IntersectionObserverCallback = (entries) => {
    if (!isAutoActive.value) return

    for (const entry of entries) {
      visibilityMap.set(entry.target as HTMLElement, entry.intersectionRatio)
    }

    updateActiveIndex()
  }

  const setItems = (elements: HTMLElement[]) => {
    if (typeof window === 'undefined' || typeof IntersectionObserver === 'undefined') return

    trackedElements = elements.filter(Boolean)
    cleanupObserver()

    if (!trackedElements.length) return

    observer = new IntersectionObserver(handleIntersections, {
      threshold: [0, 0.25, 0.5, 0.75, 1],
      rootMargin: '-20% 0px -35% 0px'
    })

    trackedElements.forEach((el) => observer?.observe(el))
  }

  const pause = () => {
    isPaused.value = true
  }

  const resume = () => {
    isPaused.value = false
    updateActiveIndex()
  }

  watch(
    prefersReducedMotion,
    (value) => {
      if (value) {
        pause()
      } else {
        resume()
      }
    },
    { immediate: true }
  )

  onScopeDispose(() => {
    cleanupObserver()
  })

  return {
    activeIndex,
    isAutoActive,
    setItems,
    pause,
    resume
  }
}
