export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore()

  if (!authStore.isAuthenticated) {
    // Allow /seller (exact path) to be public as a landing page
    // Protect /seller/* routes (like /seller/dashboard) but not /seller itself
    if (to.path === '/seller') {
      return // Allow public access to seller landing page
    }
    
    const protectedRoutes = ['/buyer', '/seller', '/admin']
    if (protectedRoutes.some((path) => to.path.startsWith(path))) {
      return navigateTo({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }
  }
})

