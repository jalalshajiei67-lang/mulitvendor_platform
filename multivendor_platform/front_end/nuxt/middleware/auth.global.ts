export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore()

  if (!authStore.isAuthenticated) {
    // Allow public access to seller landing pages
    const publicSellerRoutes = ['/seller/landing', '/seller']
    if (publicSellerRoutes.includes(to.path)) {
      return // Allow public access to seller landing pages
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

