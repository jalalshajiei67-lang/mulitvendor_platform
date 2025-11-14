/**
 * Utility functions for image URL formatting
 */

/**
 * Get backend base URL (remove /api suffix if present)
 */
const getBackendBaseUrl = (): string => {
  let apiBase = ''
  
  // Check if we're on client side
  const isClient = typeof window !== 'undefined'
  
  if (isClient) {
    // Client-side: try to get from runtime config or window
    try {
      // In Nuxt, we can access runtime config via useRuntimeConfig()
      // But in utils, we need to get it differently
      // For now, try to get from window or use default
      const config = (window as any).__NUXT__?.config?.public?.apiBase
      apiBase = config || ''
    } catch {
      // Fallback if config not available
      apiBase = ''
    }
    
    // Replace Docker hostname with localhost for local development
    if (apiBase.includes('backend:8000')) {
      apiBase = apiBase.replace('backend:8000', '127.0.0.1:8000')
    }
    
    // If API_BASE_URL ends with /api, remove it to get base URL
    if (apiBase.endsWith('/api')) {
      return apiBase.replace('/api', '')
    }
    
    // If API_BASE_URL is empty (production with relative URLs)
    if (!apiBase || apiBase === '') {
      const hostname = window.location.hostname
      if (hostname.includes('indexo.ir')) {
        return 'https://multivendor-backend.indexo.ir'
      }
      return 'http://127.0.0.1:8000'
    }
    
    return apiBase
  }
  
  // Server-side: use default or environment variable
  // In Nuxt utils, we can't use useRuntimeConfig directly
  // So we'll use environment variable or default
  apiBase = process.env.NUXT_PUBLIC_API_BASE || ''
  
  if (apiBase.endsWith('/api')) {
    return apiBase.replace('/api', '')
  }
  
  return apiBase || 'http://127.0.0.1:8000'
}

/**
 * Format image URL to absolute URL
 * @param imageData - The image URL (string) or object with image_url/image fields
 * @returns Absolute image URL or null
 */
export const formatImageUrl = (imageData: string | { image_url?: string; image?: string } | null | undefined): string | null => {
  if (!imageData) {
    return null
  }

  // If imageData is an object, prefer image_url
  if (typeof imageData === 'object') {
    if (imageData.image_url) {
      return imageData.image_url
    }
    if (imageData.image) {
      imageData = imageData.image
    } else {
      return null
    }
  }

  // imageData is now a string (URL)
  if (!imageData || typeof imageData !== 'string') {
    return null
  }

  // If already absolute URL, return as is
  if (imageData.startsWith('http://') || imageData.startsWith('https://')) {
    // In development, convert HTTPS localhost URLs to HTTP to avoid mixed content issues
    if (imageData.startsWith('https://localhost') || imageData.startsWith('https://127.0.0.1')) {
      return imageData.replace('https://', 'http://')
    }
    return imageData
  }

  // If relative URL (starts with /), prepend backend base URL
  if (imageData.startsWith('/')) {
    const backendBaseUrl = getBackendBaseUrl()
    return `${backendBaseUrl}${imageData}`
  }

  // If relative URL without leading slash, add it
  const backendBaseUrl = getBackendBaseUrl()
  return `${backendBaseUrl}/${imageData}`
}

export default formatImageUrl

