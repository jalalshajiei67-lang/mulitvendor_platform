// Frontend configuration
let apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

// Replace Docker hostname with localhost for local development
if (apiBaseUrl && apiBaseUrl.includes('backend:8000')) {
    console.warn('⚠️ Detected Docker hostname "backend:8000" in config. Using localhost instead.');
    apiBaseUrl = apiBaseUrl.replace('backend:8000', '127.0.0.1:8000');
}

// Ensure /api suffix
if (apiBaseUrl && !apiBaseUrl.endsWith('/api') && !apiBaseUrl.endsWith('/api/')) {
    if (apiBaseUrl.startsWith('http')) {
        apiBaseUrl = apiBaseUrl.endsWith('/') ? apiBaseUrl + 'api' : apiBaseUrl + '/api';
    }
}

export const config = {
    // API base URL
    apiBaseUrl: apiBaseUrl || 'http://127.0.0.1:8000/api',

    // Django admin panel URL
    djangoAdminUrl: import.meta.env.VITE_DJANGO_ADMIN_URL || 'http://127.0.0.1:8000/admin/',

    // Other configuration options can be added here
}

// Log the final API URL for debugging
console.log('🔧 API Configuration:', {
    apiBaseUrl: config.apiBaseUrl,
    envVar: import.meta.env.VITE_API_BASE_URL,
    mode: import.meta.env.MODE
});

export default config

