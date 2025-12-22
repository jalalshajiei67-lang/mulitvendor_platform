import type { FetchOptions } from 'ofetch'

const isFormData = (value: unknown): value is FormData =>
  typeof FormData !== 'undefined' && value instanceof FormData

// Simple in-memory cache for GET requests
const cache = new Map<string, { data: any; timestamp: number; ttl: number }>()
const pendingRequests = new Map<string, Promise<any>>()

interface ExtendedFetchOptions<T> extends FetchOptions<T> {
  params?: FetchOptions<T>['query']
  /**
   * If true, 404 errors will not redirect to 404 page (default: false)
   */
  skip404Redirect?: boolean
  /**
   * If true, 500 errors will not redirect to 500 page (default: false)
   */
  skip500Redirect?: boolean
  /**
   * Cache TTL in seconds (default: 0, no cache)
   */
  cache?: number
  /**
   * AbortSignal for request cancellation
   */
  signal?: AbortSignal
}

export const useApiFetch = async <T>(endpoint: string, options: ExtendedFetchOptions<T> = {}) => {
  // Validate endpoint parameter
  if (!endpoint || typeof endpoint !== 'string') {
    throw new Error(`useApiFetch: endpoint must be a non-empty string, got: ${typeof endpoint}`)
  }

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

  // For SSR (server-side), use internal Docker network hostname if available
  // This avoids SSL/network issues when frontend container tries to reach external domain
  let apiBase = config.public.apiBase.replace(/\/$/, '')
  
  if (!process.client) {
    // Server-side rendering: prefer internal Docker network hostname
    const internalApiBase = process.env.NUXT_API_BASE || process.env.NUXT_INTERNAL_API_BASE
    if (internalApiBase) {
      apiBase = internalApiBase.replace(/\/$/, '')
    } else if (apiBase.includes('api.indexo.ir') || apiBase.includes('https://')) {
      // Fallback: use internal Docker service name if external URL is configured
      // This works because all containers are on the same Docker network
      apiBase = 'http://multivendor_backend:8000/api'
    }
  }
  
  // Normalize endpoint path
  const endpointPath = endpoint.replace(/^\//, '')
  
  const url = `${apiBase}/${endpointPath}`

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

  const { params, skip404Redirect, skip500Redirect, cache: cacheTTL, signal, ...restOptions } = options

  // Check cache for GET requests
  const isGetRequest = !options.method || options.method === 'GET' || options.method === 'get'
  const cacheKey = isGetRequest ? `${url}?${new URLSearchParams(restOptions.query ?? params as any).toString()}` : null
  
  if (cacheKey && cacheTTL && cacheTTL > 0) {
    const cached = cache.get(cacheKey)
    if (cached && Date.now() - cached.timestamp < cached.ttl * 1000) {
      return cached.data as T
    }
  }

  // Check if there's a pending request for the same URL
  if (cacheKey && pendingRequests.has(cacheKey)) {
    return pendingRequests.get(cacheKey) as Promise<T>
  }

  // Create abort controller if signal not provided
  const abortController = signal ? null : new AbortController()
  const requestSignal = signal || abortController?.signal

  try {
    const requestPromise = $fetch<T>(url, {
      ...restOptions,
      query: restOptions.query ?? params,
      headers,
      credentials: restOptions.credentials ?? 'include',
      signal: requestSignal
    }).then((data) => {
      // Cache successful GET responses
      if (cacheKey && cacheTTL && cacheTTL > 0 && isGetRequest) {
        cache.set(cacheKey, {
          data,
          timestamp: Date.now(),
          ttl: cacheTTL
        })
        // Clean up old cache entries periodically
        if (cache.size > 100) {
          const now = Date.now()
          for (const [key, value] of cache.entries()) {
            if (now - value.timestamp > value.ttl * 1000) {
              cache.delete(key)
            }
          }
        }
      }
      pendingRequests.delete(cacheKey || '')
      return data
    }).catch((error) => {
      pendingRequests.delete(cacheKey || '')
      throw error
    })

    // Store pending request
    if (cacheKey) {
      pendingRequests.set(cacheKey, requestPromise)
    }

    return await requestPromise
  } catch (error: any) {
    // Handle 404 and 500 errors - redirect to appropriate error pages
    const statusCode = error?.statusCode || error?.status || error?.response?.status
    
    // Only redirect for GET requests (page resources like products, blogs, etc.)
    const isGetRequest = !options.method || options.method === 'GET' || options.method === 'get'
    
    // Don't redirect for API endpoints (auth, dashboard, etc.) - let the calling code handle the error
    const isApiEndpoint = endpointPath.startsWith('auth/') || 
                         endpointPath.startsWith('api/') ||
                         endpointPath.includes('/dashboard/') ||
                         endpointPath.includes('/orders/') ||
                         endpointPath.includes('/reviews/')
    
    if (isGetRequest && process.client && !isApiEndpoint) {
      try {
        const route = useRoute()
        
        // Handle 404 errors - redirect to 404 page
        if (statusCode === 404 && !skip404Redirect && route.path !== '/404') {
          // Navigate to 404 page - this will handle the user experience
          navigateTo('/404').catch(() => {
            // If navigation fails silently, continue with error handling
          })
        }
        
        // Handle 500 errors - redirect to 500 page
        if (statusCode === 500 && !skip500Redirect && route.path !== '/500') {
          // Navigate to 500 page - this will handle the user experience
          navigateTo('/500').catch(() => {
            // If navigation fails silently, continue with error handling
          })
        }
      } catch (navError) {
        // If navigation fails, continue with normal error handling
        console.warn('Failed to navigate to error page:', navError)
      }
    }
    
    // Re-throw the error so calling code can handle it (for cleanup, logging, etc.)
    throw error
  }
}

