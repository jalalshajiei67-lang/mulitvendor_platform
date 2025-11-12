/**
 * Authentication API composable
 * Handles login, logout, register, and profile management
 */

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  password2?: string
  first_name?: string
  last_name?: string
  role?: 'buyer' | 'seller'
}

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  role: string
  is_staff: boolean
  is_superuser: boolean
  profile?: any
  vendor_profile?: any
}

export const useAuthApi = () => {
  return {
    // Authentication
    async login(credentials: LoginCredentials) {
      return useApiFetch<{ token: string; user: User }>('auth/login/', {
        method: 'POST',
        body: credentials
      })
    },

    async logout() {
      return useApiFetch('auth/logout/', {
        method: 'POST'
      })
    },

    async register(userData: RegisterData) {
      return useApiFetch<{ token: string; user: User }>('auth/register/', {
        method: 'POST',
        body: userData
      })
    },

    // User Profile
    async getCurrentUser() {
      return useApiFetch<User>('auth/me/')
    },

    async updateProfile(data: FormData | Record<string, any>) {
      return useApiFetch('auth/profile/update/', {
        method: 'PUT',
        body: data
      })
    },

    // Password Management
    async changePassword(data: {
      old_password: string
      new_password: string
      new_password2: string
    }) {
      return useApiFetch('auth/change-password/', {
        method: 'POST',
        body: data
      })
    },

    async resetPassword(email: string) {
      return useApiFetch('auth/password-reset/', {
        method: 'POST',
        body: { email }
      })
    },

    async confirmPasswordReset(data: {
      token: string
      password: string
      password2: string
    }) {
      return useApiFetch('auth/password-reset/confirm/', {
        method: 'POST',
        body: data
      })
    }
  }
}



