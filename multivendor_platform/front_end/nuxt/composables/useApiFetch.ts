import type { FetchOptions } from 'ofetch'

const isFormData = (value: unknown): value is FormData =>
  typeof FormData !== 'undefined' && value instanceof FormData

export const useApiFetch = async <T>(endpoint: string, options: FetchOptions<T> = {}) => {
  // Try to get Nuxt app - if not available during SSR, handle gracefully
  let config: any
  let authToken: string | null = null

  try {
    // Check if we have a Nuxt app instance available
    const nuxtApp = tryUseNuxtApp()
    
    if (nuxtApp) {
      // We're in a proper Nuxt context, use composables
      config = useRuntimeConfig()
      
      // Get auth token from localStorage first (client-side), then fallback to cookie
      if (process.client) {
        authToken = window.localStorage.getItem('authToken')
        if (!authToken) {
          const cookie = useCookie<string | null>('authToken')
          authToken = cookie.value ?? null
        }
      } else {
        // Server-side: use cookie
        const cookie = useCookie<string | null>('authToken')
        authToken = cookie.value ?? null
      }
    } else {
      // No Nuxt context available, use environment variables or defaults
      config = {
        public: {
          apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'
        }
      }
    }
  } catch (error) {
    // Fallback if composables fail
    config = {
      public: {
        apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'
      }
    }
  }

  const apiBase = config.public.apiBase.replace(/\/$/, '')
  const url = `${apiBase}/${endpoint.replace(/^\//, '')}`

  const headers: Record<string, string> = {
    Accept: 'application/json',
    ...(options?.headers as Record<string, string> | undefined)
  }

  if (!isFormData(options?.body)) {
    headers['Content-Type'] = headers['Content-Type'] ?? 'application/json'
  }

  if (authToken) {
    headers.Authorization = `Token ${authToken}`
  } else {
    // For guest users, include guest session ID in headers if available
    if (process.client) {
      const guestSessionId = window.localStorage.getItem('chatGuestSession')
      if (guestSessionId) {
        headers['X-Guest-Session-ID'] = guestSessionId
      }
    }
  }

  type ExtendedFetchOptions = FetchOptions<T> & { params?: FetchOptions<T>['query'] }
  const { params, ...restOptions } = (options ?? {}) as ExtendedFetchOptions

  return $fetch<T>(url, {
    ...restOptions,
    query: restOptions.query ?? params,
    headers,
    credentials: restOptions.credentials ?? 'include'
  })
}

