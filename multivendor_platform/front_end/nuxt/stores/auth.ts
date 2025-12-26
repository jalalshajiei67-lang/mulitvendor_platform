import type { AuthError } from '~/utils/authErrors'
import { handleAuthError } from '~/utils/authErrors'

type AuthUser = Record<string, any>
type LoginResponse = { token: string; user: AuthUser }

const AUTH_TOKEN_COOKIE = 'authToken'
const AUTH_USER_COOKIE = 'authUser'

// Helper to safely check if we're in production
const isProduction = () => {
  if (typeof process !== 'undefined' && process.env) {
    return process.env.NODE_ENV === 'production'
  }
  if (typeof import.meta !== 'undefined' && import.meta.env) {
    return import.meta.env.PROD === true
  }
  return false
}

const parseUser = (raw: string | null | undefined | any): AuthUser | null => {
  if (!raw) {
    return null
  }
  
  // If it's already an object, return it
  if (typeof raw === 'object' && !Array.isArray(raw) && raw !== null) {
    return raw as AuthUser
  }
  
  // If it's not a string, try to convert it
  if (typeof raw !== 'string') {
    console.warn('parseUser received non-string value:', typeof raw, raw)
    return null
  }
  
  try {
    // Trim whitespace and check if it's valid JSON
    const trimmed = raw.trim()
    if (!trimmed || trimmed === 'null' || trimmed === 'undefined') {
      return null
    }
    return JSON.parse(trimmed)
  } catch (error) {
    console.warn('Unable to parse stored auth user payload', error)
    // Clear invalid data from localStorage if on client
    if (process.client) {
      try {
        localStorage.removeItem('user')
        localStorage.removeItem('authToken')
      } catch (e) {
        // Ignore localStorage errors
      }
    }
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
          secure: isProduction(),
          maxAge: 60 * 60 * 24 * 30, // 30 days
          httpOnly: false // Must be false for client-side access
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
          secure: isProduction(),
          maxAge: 60 * 60 * 24 * 30, // 30 days
          httpOnly: false // Must be false for client-side access
        })
      } catch (error) {
        // Nuxt context not available yet
        console.warn('Unable to access user cookie:', error)
        return null
      }
    }
    return userCookie
  }

  // Initialize from cookies (works on both server and client)
  // Then sync to localStorage on client
  let initialToken: string | null = null
  let initialUser: AuthUser | null = null

  try {
    const tokenCookie = useCookie<string | null>(AUTH_TOKEN_COOKIE, {
      sameSite: 'lax',
      secure: isProduction(),
      maxAge: 60 * 60 * 24 * 30, // 30 days
      httpOnly: false
    })
    const userCookie = useCookie<string | null>(AUTH_USER_COOKIE, {
      sameSite: 'lax',
      secure: isProduction(),
      maxAge: 60 * 60 * 24 * 30, // 30 days
      httpOnly: false
    })
    
    if (tokenCookie.value) {
      // Ensure token is a string
      const tokenValue = tokenCookie.value
      initialToken = typeof tokenValue === 'string' ? tokenValue : String(tokenValue || '')
      if (!initialToken) {
        initialToken = null
      }
    }
    
    if (userCookie.value) {
      const parsed = parseUser(userCookie.value)
      if (parsed) {
        initialUser = parsed
      } else {
        // Clear invalid cookie
        (userCookie as any).value = null
        // Also clear token if user is invalid
        if (tokenCookie.value) {
          (tokenCookie as any).value = null
          initialToken = null
        }
      }
    }
    
    // On client, sync cookies to localStorage for consistency
    if (process.client && initialToken) {
      try {
        localStorage.setItem('authToken', initialToken)
        if (initialUser) {
          localStorage.setItem('user', JSON.stringify(initialUser))
        }
      } catch (e) {
        // Ignore localStorage errors
      }
    }
  } catch (error) {
    // Cookie access might fail, try localStorage as fallback (client only)
    if (process.client) {
      try {
        initialToken = localStorage.getItem('authToken')
        initialUser = parseUser(localStorage.getItem('user'))
      } catch (e) {
        // Ignore localStorage errors
      }
    }
    console.warn('Unable to access cookies during initialization:', error)
  }

  const token = ref<string | null>(initialToken)
  const user = ref<AuthUser | null>(initialUser)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const authError = ref<AuthError | null>(null)
  const hydrated = ref(false)

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
      (tokenCookie as any).value = nextToken
    }
    if (userCookie) {
      (userCookie as any).value = nextUser ? JSON.stringify(nextUser) : null
    }
    setClientStorage(nextToken, nextUser)
  }

  const login = async (credentials: Record<string, any>) => {
    loading.value = true
    error.value = null
    authError.value = null

    try {
      const response = await useApiFetch<LoginResponse>('auth/login/', {
        method: 'POST',
        body: credentials
      })
      persistSession(response.token, response.user)
      return response
    } catch (err: any) {
      const handledError = handleAuthError(err)
      authError.value = handledError
      error.value = handledError.message
      console.error('Login error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    loading.value = true

    // Clear session immediately for instant UI feedback
    persistSession(null, null)
    
    // Call logout API in background (fire-and-forget)
    // Don't wait for it to complete - user is already logged out locally
    useApiFetch<void>('auth/logout/', { method: 'POST' })
      .catch(err => {
        // Silently handle errors - user is already logged out locally
        console.warn('Logout API error (non-blocking):', err)
      })
      .finally(() => {
        loading.value = false
      })
  }

  const register = async (payload: Record<string, any>) => {
    loading.value = true
    error.value = null
    authError.value = null

    try {
      const response = await useApiFetch<LoginResponse>('auth/register/', {
        method: 'POST',
        body: payload
      })
      persistSession(response.token, response.user)
      return response
    } catch (err: any) {
      const handledError = handleAuthError(err)
      authError.value = handledError
      error.value = handledError.message
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
    // Mark as hydrated on client
    if (process.client) {
      hydrated.value = true
    }
    
    // If we have a token but no user, fetch the user
    if (token.value && !user.value) {
      await fetchCurrentUser().catch(() => {
        /* handled in fetchCurrentUser */
      })
      return
    }
    
    // If we don't have a token, try to restore from cookies (client-side only)
    if (!token.value && process.client) {
      try {
        const tokenCookie = useCookie<string | null>(AUTH_TOKEN_COOKIE, {
          sameSite: 'lax',
          secure: isProduction(),
          maxAge: 60 * 60 * 24 * 30, // 30 days
          httpOnly: false
        })
        const userCookie = useCookie<string | null>(AUTH_USER_COOKIE, {
          sameSite: 'lax',
          secure: isProduction(),
          maxAge: 60 * 60 * 24 * 30, // 30 days
          httpOnly: false
        })
        
        if (tokenCookie.value) {
          // Ensure token is a string
          const tokenValue = tokenCookie.value
          const restoredToken = typeof tokenValue === 'string' ? tokenValue : String(tokenValue || '')
          const restoredUser = parseUser(userCookie.value)
          
          // If user cookie is invalid, clear both cookies
          if (userCookie && userCookie.value && !restoredUser) {
            (userCookie as any).value = null
            if (tokenCookie) {
              (tokenCookie as any).value = null
            }
            // Clear localStorage as well
            try {
              localStorage.removeItem('authToken')
              localStorage.removeItem('user')
            } catch (e) {
              // Ignore localStorage errors
            }
            return
          }
          
          // Restore to localStorage for consistency
          if (restoredToken) {
            try {
              localStorage.setItem('authToken', restoredToken)
              if (restoredUser) {
                localStorage.setItem('user', JSON.stringify(restoredUser))
              }
            } catch (e) {
              // Ignore localStorage errors
            }
          }
          
          // Update store state
          persistSession(restoredToken, restoredUser)
          
          // Optionally verify the token is still valid by fetching current user
          // This will update user data if it has changed
          await fetchCurrentUser().catch(() => {
            /* If token is invalid, fetchCurrentUser will handle logout */
          })
        }
      } catch (error) {
        console.warn('Unable to restore auth from cookies:', error)
      }
    }
  }

  const clearError = () => {
    error.value = null
    authError.value = null
  }

  // OTP Methods
  const requestOtpLogin = async (phone: string) => {
    loading.value = true
    error.value = null
    authError.value = null

    try {
      const { useOtpApi } = await import('~/composables/useOtpApi')
      const otpApi = useOtpApi()
      const response = await otpApi.requestOtp({
        phone,
        purpose: 'login'
      })
      return response
    } catch (err: any) {
      const handledError = handleAuthError(err)
      authError.value = handledError
      error.value = handledError.message
      console.error('OTP request error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const verifyOtpLogin = async (phone: string, code: string, firstName?: string, lastName?: string) => {
    loading.value = true
    error.value = null
    authError.value = null

    try {
      const { useOtpApi } = await import('~/composables/useOtpApi')
      const otpApi = useOtpApi()
      const response = await otpApi.verifyOtp({
        phone,
        code,
        purpose: 'login',
        first_name: firstName,
        last_name: lastName
      })
      
      if (response.success && response.token && response.user) {
        persistSession(response.token, response.user)
      }
      
      return response
    } catch (err: any) {
      const handledError = handleAuthError(err)
      authError.value = handledError
      error.value = handledError.message
      console.error('OTP verification error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const requestPasswordResetOtp = async (phone: string) => {
    loading.value = true
    error.value = null
    authError.value = null

    try {
      const { useOtpApi } = await import('~/composables/useOtpApi')
      const otpApi = useOtpApi()
      const response = await otpApi.requestOtp({
        phone,
        purpose: 'password_reset'
      })
      return response
    } catch (err: any) {
      const handledError = handleAuthError(err)
      authError.value = handledError
      error.value = handledError.message
      console.error('Password reset OTP request error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // Set hydrated immediately on client if we have initial values
  if (process.client && (initialToken || initialUser)) {
    hydrated.value = true
  }

  return {
    token,
    user,
    loading,
    error,
    authError,
    hydrated,
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
    initializeAuth,
    clearError,
    requestOtpLogin,
    verifyOtpLogin,
    requestPasswordResetOtp
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))
}

