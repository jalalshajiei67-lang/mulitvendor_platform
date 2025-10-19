// Frontend configuration
export const config = {
    // API base URL
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',

    // Django admin panel URL
    djangoAdminUrl: import.meta.env.VITE_DJANGO_ADMIN_URL || 'http://127.0.0.1:8000/admin/',

    // Other configuration options can be added here
}

export default config

