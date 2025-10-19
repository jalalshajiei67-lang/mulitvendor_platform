// src/composables/useDebounce.js
import { ref, watch } from 'vue'

/**
 * Composable for debouncing a value
 * @param {Ref} value - The reactive value to debounce
 * @param {number} delay - The delay in milliseconds (default: 500)
 * @returns {Ref} - The debounced value
 */
export function useDebounce(value, delay = 500) {
    const debouncedValue = ref(value.value)
    let timeout = null

    watch(value, (newValue) => {
        if (timeout) {
            clearTimeout(timeout)
        }

        timeout = setTimeout(() => {
            debouncedValue.value = newValue
        }, delay)
    })

    return debouncedValue
}

/**
 * Function to create a debounced function
 * @param {Function} fn - The function to debounce
 * @param {number} delay - The delay in milliseconds (default: 500)
 * @returns {Function} - The debounced function
 */
export function debounce(fn, delay = 500) {
    let timeout = null

    return function (...args) {
        if (timeout) {
            clearTimeout(timeout)
        }

        timeout = setTimeout(() => {
            fn.apply(this, args)
        }, delay)
    }
}

