import type { FetchOptions } from 'ofetch'

const isFormData = (value: unknown): value is FormData =>
  typeof FormData !== 'undefined' && value instanceof FormData

interface ExtendedFetchOptions<T> extends FetchOptions<T> {
  params?: FetchOptions<T>['query']
  /**
   * If true, 404 errors will not redirect to 404 page (default: false)
   */
  skip404Redirect?: boolean
  /**
   * If true, disable retry logic for this request (default: false)
   * Retry is enabled by default for GET requests during SSR
   */
  disableRetry?: boolean
}

/**
 * Retry a function with exponential backoff
 * @param fn Function to retry
 * @param maxRetries Maximum number of retry attempts (default: 3)
 * @param baseDelay Base delay in milliseconds (default: 100)
 * @returns Promise that resolves with the function result
 */
const retryWithBackoff = async <T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 100
): Promise<T> => {
  let lastError: any
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn()
    } catch (error: any) {
      lastError = error
      
      // Don't retry on last attempt
      if (attempt >= maxRetries) {
        break
      }
      
      // Check if error is retryable (network errors, 404, 500-504)
      const statusCode = error?.statusCode || error?.status || error?.response?.status
      const isRetryable = 
        !statusCode || // Network error (no status code)
        statusCode === 404 || // Not found (might be temporary)
        (statusCode >= 500 && statusCode <= 504) // Server errors
      
      // Don't retry on authentication/authorization errors
      if (statusCode === 401 || statusCode === 403) {
        break
      }
      
      // Only retry retryable errors
      if (!isRetryable) {
        break
      }
      
      // Calculate delay with exponential backoff
      const delay = baseDelay * Math.pow(2, attempt)
      
      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
  
  // All retries failed, throw the last error
  throw lastError
}

export const useApiFetch = async <T>(endpoint: string, options: ExtendedFetchOptions<T> = {}) => {
  // #region agent log
  fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useApiFetch.ts:14',message:'useApiFetch entry',data:{endpoint,method:options?.method||'GET',hasBody:!!options?.body},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'E'})}).catch(()=>{});
  // #endregion
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
  
  // Normalize endpoint path (remove leading slash if present)
  const endpointPath = endpoint.replace(/^\//, '')
  
  const url = `${apiBase}/${endpointPath}`
  // #region agent log
  fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useApiFetch.ts:61',message:'useApiFetch URL constructed',data:{url,hasAuthToken:!!authToken,hasQuery:!!(options?.query||options?.params)},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'B'})}).catch(()=>{});
  // #endregion

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

  const { params, skip404Redirect, disableRetry, ...restOptions } = options

  // Determine if retry should be enabled
  // Default: enabled for GET requests during SSR, disabled otherwise
  const isGetRequest = !restOptions.method || restOptions.method === 'GET' || restOptions.method === 'get'
  const shouldRetry = !disableRetry && isGetRequest && !process.client

  const fetchRequest = async (): Promise<T> => {
    const finalQuery = restOptions.query ?? params
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useApiFetch.ts:87',message:'useApiFetch before request',data:{url,method:restOptions.method||'GET',hasQuery:!!finalQuery,queryKeys:finalQuery?Object.keys(finalQuery):[]},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'B'})}).catch(()=>{});
    // #endregion
    const response = await $fetch<T>(url, {
      ...restOptions,
      query: finalQuery,
      headers,
      credentials: restOptions.credentials ?? 'include'
    })
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useApiFetch.ts:95',message:'useApiFetch success',data:{endpoint,responseType:typeof response,isArray:Array.isArray(response),hasResults:'results' in (response as any)},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
    // #endregion
    return response
  }

  try {
    // Use retry logic if enabled, otherwise make direct request
    const response = shouldRetry 
      ? await retryWithBackoff(fetchRequest, 3, 100)
      : await fetchRequest()
    return response
  } catch (error: any) {
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'useApiFetch.ts:99',message:'useApiFetch error',data:{endpoint,statusCode:error?.statusCode||error?.status||error?.response?.status,errorMessage:error?.message,hasData:!!error?.data},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
    // #endregion
    // Handle 404 errors - redirect to 404 page
    const statusCode = error?.statusCode || error?.status || error?.response?.status
    
    if (statusCode === 404 && !skip404Redirect) {
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
          // Check if we're already on the 404 page to avoid redirect loops
          if (route.path !== '/404') {
            // Navigate to 404 page - this will handle the user experience
            navigateTo('/404').catch(() => {
              // If navigation fails silently, continue with error handling
            })
          }
        } catch (navError) {
          // If navigation fails, continue with normal error handling
          console.warn('Failed to navigate to 404 page:', navError)
        }
      }
    }
    
    // Re-throw the error so calling code can handle it (for cleanup, logging, etc.)
    throw error
  }
}

