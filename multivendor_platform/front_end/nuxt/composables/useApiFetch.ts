import type { FetchOptions } from 'ofetch'

const isFormData = (value: unknown): value is FormData =>
  typeof FormData !== 'undefined' && value instanceof FormData

export const useApiFetch = async <T>(endpoint: string, options: FetchOptions<T> = {}) => {
  // Get runtime config - must be called within Nuxt context
  // This will throw if called outside proper context, which is the desired behavior
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase.replace(/\/$/, '')
  const url = `${apiBase}/${endpoint.replace(/^\//, '')}`

  let authToken: string | null = null

  // Get auth token from localStorage first (client-side), then fallback to cookie
  if (process.client) {
    authToken = window.localStorage.getItem('authToken')
    if (!authToken) {
      // Only try cookie if localStorage doesn't have it
      // useCookie must be called within Nuxt context
      const cookie = useCookie<string | null>('authToken')
      authToken = cookie.value ?? null
    }
  } else {
    // Server-side: use cookie (must be in Nuxt context)
    const cookie = useCookie<string | null>('authToken')
    authToken = cookie.value ?? null
  }

  const headers: Record<string, string> = {
    Accept: 'application/json',
    ...(options?.headers as Record<string, string> | undefined)
  }

  if (!isFormData(options?.body)) {
    headers['Content-Type'] = headers['Content-Type'] ?? 'application/json'
  }

  if (authToken) {
    headers.Authorization = `Token ${authToken}`
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

