export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore()

  if (!authStore.isAuthenticated) {
    const protectedRoutes = ['/buyer', '/seller', '/admin']
    if (protectedRoutes.some((path) => to.path.startsWith(path))) {
      return navigateTo({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }
  }
})

