// Utility function to format image URLs
// Converts relative image URLs to absolute URLs using the backend base URL

// Get backend base URL (remove /api suffix if present)
const getBackendBaseUrl = () => {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '';
  
  // If API_BASE_URL ends with /api, remove it to get base URL
  if (apiBaseUrl.endsWith('/api')) {
    return apiBaseUrl.replace('/api', '');
  }
  
  // If API_BASE_URL is empty (production with relative URLs), 
  // we need to determine the backend URL from the current origin or use a default
  if (!apiBaseUrl || apiBaseUrl === '') {
    // In production, try to get from window location or use the known backend URL
    if (typeof window !== 'undefined') {
      // Check if we're on the production domain
      const hostname = window.location.hostname;
      if (hostname.includes('indexo.ir')) {
        return 'http://multivendor-backend.indexo.ir';
      }
    }
    // Default to local development
    return 'http://127.0.0.1:8000';
  }
  
  // Return as is (might already be the base URL)
  return apiBaseUrl;
};

/**
 * Format image URL to absolute URL
 * @param {string} imageUrl - The image URL (can be relative or absolute)
 * @returns {string} - Absolute image URL
 */
export const formatImageUrl = (imageUrl) => {
  if (!imageUrl) {
    return null;
  }
  
  // If already absolute URL, return as is
  if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
    return imageUrl;
  }
  
  // If relative URL (starts with /), prepend backend base URL
  if (imageUrl.startsWith('/')) {
    const backendBaseUrl = getBackendBaseUrl();
    return `${backendBaseUrl}${imageUrl}`;
  }
  
  // If relative URL without leading slash, add it
  const backendBaseUrl = getBackendBaseUrl();
  return `${backendBaseUrl}/${imageUrl}`;
};

export default formatImageUrl;

