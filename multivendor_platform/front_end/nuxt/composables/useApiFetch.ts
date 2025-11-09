import type { FetchOptions } from 'ofetch'

const isFormData = (value: unknown): value is FormData =>
  typeof FormData !== 'undefined' && value instanceof FormData

export const useApiFetch = async <T>(endpoint: string, options: FetchOptions<T> = {}) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase.replace(/\/$/, '')
  const url = `${apiBase}/${endpoint.replace(/^\//, '')}`

  let authToken: string | null = null

  if (process.client) {
    authToken = window.localStorage.getItem('authToken')
    if (!authToken) {
      authToken = useCookie<string | null>('authToken').value ?? null
    }
  } else {
    authToken = useCookie<string | null>('authToken').value ?? null
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

  return $fetch<T>(url, {
    ...options,
    headers,
    credentials: options?.credentials ?? 'include'
  })
}

