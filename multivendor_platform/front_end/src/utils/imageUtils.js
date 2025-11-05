// Utility function to format image URLs
// Converts relative image URLs to absolute URLs using the backend base URL

// Get backend base URL (remove /api suffix if present)
const getBackendBaseUrl = () => {
  let apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '';

  // Replace Docker hostname with localhost for local development
  if (apiBaseUrl && apiBaseUrl.includes('backend:8000')) {
    apiBaseUrl = apiBaseUrl.replace('backend:8000', '127.0.0.1:8000');
  }

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
        // Use HTTPS for production
        return 'https://multivendor-backend.indexo.ir';
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
 * @param {string|object} imageData - The image URL (string) or object with image_url/image fields
 * @returns {string} - Absolute image URL
 */
export const formatImageUrl = (imageData) => {
  if (!imageData) {
    return null;
  }

  // If imageData is an object (e.g., category/department object), prefer image_url
  if (typeof imageData === 'object') {
    // Prefer image_url if available (from backend serializer)
    if (imageData.image_url) {
      return imageData.image_url;
    }
    // Fall back to image field
    if (imageData.image) {
      imageData = imageData.image;
    } else {
      return null;
    }
  }

  // imageData is now a string (URL)
  if (!imageData) {
    return null;
  }

  // If already absolute URL, return as is
  if (imageData.startsWith('http://') || imageData.startsWith('https://')) {
    return imageData;
  }

  // If relative URL (starts with /), prepend backend base URL
  if (imageData.startsWith('/')) {
    const backendBaseUrl = getBackendBaseUrl();
    return `${backendBaseUrl}${imageData}`;
  }

  // If relative URL without leading slash, add it
  const backendBaseUrl = getBackendBaseUrl();
  return `${backendBaseUrl}/${imageData}`;
};

export default formatImageUrl;

