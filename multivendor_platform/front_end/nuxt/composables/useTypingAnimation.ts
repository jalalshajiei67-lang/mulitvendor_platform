import { ref, readonly, onUnmounted } from 'vue'

/**
 * Composable for creating typing animation effect
 * Cycles through multiple texts with typing and deleting animation
 */
export const useTypingAnimation = (
  texts: string[],
  options: {
    typingSpeed?: number // milliseconds per character
    deletingSpeed?: number // milliseconds per character
    pauseAfterTyping?: number // milliseconds to pause after typing
    pauseAfterDeleting?: number // milliseconds to pause after deleting
    startDelay?: number // milliseconds before starting animation
  } = {}
) => {
  const {
    typingSpeed = 100,
    deletingSpeed = 50,
    pauseAfterTyping = 2000,
    pauseAfterDeleting = 500,
    startDelay = 1000
  } = options

  const currentText = ref('')
  const currentIndex = ref(0)
  const isTyping = ref(false)
  const isDeleting = ref(false)
  const isPaused = ref(false)

  let timeoutId: NodeJS.Timeout | null = null

  const clearTimeout = () => {
    if (timeoutId) {
      clearTimeout(timeoutId)
      timeoutId = null
    }
  }

  const type = (startFrom?: number) => {
    isTyping.value = true
    isDeleting.value = false
    isPaused.value = false

    const text = texts[currentIndex.value]
    let charIndex = startFrom ?? currentText.value.length

    const typeChar = () => {
      if (charIndex < text.length) {
        currentText.value = text.substring(0, charIndex + 1)
        charIndex++
        timeoutId = setTimeout(typeChar, typingSpeed)
      } else {
        isTyping.value = false
        isPaused.value = true
        timeoutId = setTimeout(deleteText, pauseAfterTyping)
      }
    }

    typeChar()
  }

  const deleteText = (startFrom?: number) => {
    isTyping.value = false
    isDeleting.value = true
    isPaused.value = false

    const text = texts[currentIndex.value]
    let charIndex = startFrom ?? currentText.value.length

    const deleteChar = () => {
      if (charIndex > 0) {
        currentText.value = text.substring(0, charIndex - 1)
        charIndex--
        timeoutId = setTimeout(deleteChar, deletingSpeed)
      } else {
        isDeleting.value = false
        isPaused.value = true
        currentIndex.value = (currentIndex.value + 1) % texts.length
        timeoutId = setTimeout(type, pauseAfterDeleting)
      }
    }

    deleteChar()
  }

  const start = () => {
    clearTimeout()
    currentText.value = ''
    currentIndex.value = 0
    isTyping.value = false
    isDeleting.value = false
    isPaused.value = false
    timeoutId = setTimeout(type, startDelay)
  }

  const stop = () => {
    clearTimeout()
    currentText.value = ''
    isTyping.value = false
    isDeleting.value = false
    isPaused.value = false
  }

  const pause = () => {
    clearTimeout()
    isPaused.value = true
  }

  const resume = () => {
    if (isPaused.value) {
      const text = texts[currentIndex.value]
      const currentLength = currentText.value.length
      
      // If text is empty, start typing from beginning
      if (currentLength === 0) {
        type(0)
      }
      // If text matches full target, start deleting from end
      else if (currentText.value === text) {
        deleteText(text.length)
      }
      // Otherwise, continue typing from current position
      else {
        type(currentLength)
      }
    }
  }

  onUnmounted(() => {
    clearTimeout()
  })

  return {
    currentText: readonly(currentText),
    isTyping: readonly(isTyping),
    isDeleting: readonly(isDeleting),
    isPaused: readonly(isPaused),
    start,
    stop,
    pause,
    resume
  }
}

