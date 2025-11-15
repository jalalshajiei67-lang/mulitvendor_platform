type AuthUser = Record<string, any>
type LoginResponse = { token: string; user: AuthUser }

const AUTH_TOKEN_COOKIE = 'authToken'
const AUTH_USER_COOKIE = 'authUser'

const parseUser = (raw: string | null | undefined): AuthUser | null => {
  if (!raw) {
    return null
  }
  try {
    return JSON.parse(raw)
  } catch (error) {
    console.warn('Unable to parse stored auth user payload', error)
    return null
  }
}

const setClientStorage = (token: string | null, user: AuthUser | null) => {
  if (!process.client) return
  if (token) {
    localStorage.setItem('authToken', token)
  } else {
    localStorage.removeItem('authToken')
  }
  if (user) {
    localStorage.setItem('user', JSON.stringify(user))
  } else {
    localStorage.removeItem('user')
  }
}

export const useAuthStore = defineStore('auth', () => {
  // Lazy initialization for cookies - only access when needed
  let tokenCookie: ReturnType<typeof useCookie<string | null>> | null = null
  let userCookie: ReturnType<typeof useCookie<string | null>> | null = null

  const getTokenCookie = () => {
    if (!tokenCookie) {
      try {
        tokenCookie = useCookie<string | null>(AUTH_TOKEN_COOKIE, {
          sameSite: 'lax',
          secure: process.env.NODE_ENV === 'production'
        })
      } catch (error) {
        // Nuxt context not available yet
        console.warn('Unable to access token cookie:', error)
        return null
      }
    }
    return tokenCookie
  }

  const getUserCookie = () => {
    if (!userCookie) {
      try {
        userCookie = useCookie<string | null>(AUTH_USER_COOKIE, {
          sameSite: 'lax',
          secure: process.env.NODE_ENV === 'production'
        })
      } catch (error) {
        // Nuxt context not available yet
        console.warn('Unable to access user cookie:', error)
        return null
      }
    }
    return userCookie
  }

  // Initialize from localStorage first (client-side only)
  // Cookies will be accessed lazily when needed (not during initialization)
  let initialToken: string | null = null
  let initialUser: AuthUser | null = null

  if (process.client) {
    initialToken = localStorage.getItem('authToken')
    initialUser = parseUser(localStorage.getItem('user'))
  }
  
  // Note: We don't access cookies during initialization to avoid context issues
  // Cookies will be accessed lazily when persistSession is called or when needed

  const token = ref<string | null>(initialToken)
  const user = ref<AuthUser | null>(initialUser)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => Boolean(token.value && user.value))
  const userRole = computed(() => user.value?.role ?? null)
  const isBuyer = computed(() => userRole.value === 'buyer' || userRole.value === 'both')
  const isSeller = computed(() => userRole.value === 'seller' || userRole.value === 'both')
  const isAdmin = computed(() => Boolean(user.value?.is_staff))
  const isVerified = computed(() => Boolean(user.value?.is_verified))
  const vendorProfile = computed(() => user.value?.vendor_profile ?? null)

  const persistSession = (nextToken: string | null, nextUser: AuthUser | null) => {
    token.value = nextToken
    user.value = nextUser
    // Lazy access to cookies - only set when needed
    const tokenCookie = getTokenCookie()
    const userCookie = getUserCookie()
    if (tokenCookie) {
      tokenCookie.value = nextToken
    }
    if (userCookie) {
      userCookie.value = nextUser ? JSON.stringify(nextUser) : null
    }
    setClientStorage(nextToken, nextUser)
  }

  const login = async (credentials: Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<LoginResponse>('auth/login/', {
        method: 'POST',
        body: credentials
      })
      persistSession(response.token, response.user)
      return response
    } catch (err: any) {
      error.value =
        err?.data?.error ?? 'خطا در ورود. لطفاً اطلاعات خود را بررسی کنید.'
      console.error('Login error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    loading.value = true

    try {
      await useApiFetch<void>('auth/logout/', { method: 'POST' })
    } catch (err) {
      console.warn('Logout error:', err)
    } finally {
      persistSession(null, null)
      loading.value = false
    }
  }

  const register = async (payload: Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const response = await useApiFetch<LoginResponse>('auth/register/', {
        method: 'POST',
        body: payload
      })
      persistSession(response.token, response.user)
      return response
    } catch (err: any) {
      error.value = err?.data?.error ?? 'خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.'
      console.error('Registration error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchCurrentUser = async () => {
    if (!token.value) return null

    try {
      const data = await useApiFetch<AuthUser>('auth/me/')
      persistSession(token.value, data)
      return data
    } catch (err: any) {
      console.error('Fetch current user error:', err)
      if (err?.response?.status === 401) {
        await logout()
      }
      throw err
    }
  }

  const updateProfile = async (payload: FormData | Record<string, any>) => {
    loading.value = true
    error.value = null

    try {
      const data = await useApiFetch<AuthUser>('auth/profile/update/', {
        method: 'PUT',
        body: payload as any
      })
      persistSession(token.value, data)
      return data
    } catch (err: any) {
      error.value = 'خطا در بروزرسانی پروفایل. لطفاً دوباره تلاش کنید.'
      console.error('Profile update error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const initializeAuth = async () => {
    if (token.value && !user.value) {
      await fetchCurrentUser().catch(() => {
        /* handled in fetchCurrentUser */
      })
    }
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    userRole,
    isBuyer,
    isSeller,
    isAdmin,
    isVerified,
    vendorProfile,
    login,
    logout,
    register,
    fetchCurrentUser,
    updateProfile,
    initializeAuth
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))
}

