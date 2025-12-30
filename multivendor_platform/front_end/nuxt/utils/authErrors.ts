/**
 * Authentication Error Handler Utility
 * Provides user-friendly Persian error messages and helpful hints
 * Optimized for non-technical users over 40 years old
 */

export interface AuthError {
  message: string
  hint?: string
  type: 'network' | 'credentials' | 'validation' | 'blocked' | 'server' | 'unknown'
  field?: string
  recoverable: boolean
  action?: string
}

/**
 * Maps HTTP status codes and error types to user-friendly Persian messages
 */
export function handleAuthError(error: any): AuthError {
  // Network errors (no connection, timeout, etc.)
  if (!error || error.message?.includes('fetch') || error.message?.includes('network') || error.message?.includes('Failed to fetch')) {
    return {
      message: 'ارتباط با سرور برقرار نشد',
      hint: 'لطفاً اتصال اینترنت خود را بررسی کنید و دوباره تلاش کنید.',
      type: 'network',
      recoverable: true,
      action: 'retry'
    }
  }

  // Timeout errors
  if (error.message?.includes('timeout') || error.code === 'ECONNABORTED') {
    return {
      message: 'زمان اتصال به سرور به پایان رسید',
      hint: 'لطفاً چند لحظه صبر کنید و دوباره تلاش کنید.',
      type: 'network',
      recoverable: true,
      action: 'retry'
    }
  }

  // HTTP status code errors
  const status = error?.status || error?.response?.status || error?.statusCode || error?.data?.status

  // 400 Bad Request - Validation errors
  if (status === 400) {
    const errorData = error?.data || error?.response?.data || {}
    const errorMessage = errorData?.error || errorData?.message

    // Check if it's a field-specific validation error
    if (typeof errorData === 'object' && !errorMessage) {
      const firstField = Object.keys(errorData)[0]
      const firstError = Array.isArray(errorData[firstField]) 
        ? errorData[firstField][0] 
        : errorData[firstField]

      return {
        message: firstError || 'اطلاعات وارد شده صحیح نیست',
        hint: 'لطفاً تمام فیلدها را با دقت پر کنید.',
        type: 'validation',
        field: firstField,
        recoverable: true
      }
    }

    return {
      message: errorMessage || 'اطلاعات وارد شده صحیح نیست',
      hint: 'لطفاً تمام فیلدها را با دقت بررسی کنید و دوباره تلاش کنید.',
      type: 'validation',
      recoverable: true
    }
  }

  // 401 Unauthorized - Invalid credentials
  if (status === 401) {
    const errorMessage = error?.data?.error || error?.response?.data?.error || 'نام کاربری یا رمز عبور اشتباه است'
    return {
      message: errorMessage,
      hint: 'اگر رمز عبور خود را فراموش کرده‌اید، می‌توانید آن را بازیابی کنید.',
      type: 'credentials',
      recoverable: true,
      action: 'forgot_password'
    }
  }

  // 403 Forbidden - Account blocked
  if (status === 403) {
    const errorMessage = error?.data?.error || error?.response?.data?.error || 'حساب کاربری شما مسدود شده است'
    return {
      message: errorMessage,
      hint: 'برای رفع مشکل با پشتیبانی تماس بگیرید.',
      type: 'blocked',
      recoverable: false,
      action: 'contact_support'
    }
  }

  // 404 Not Found
  if (status === 404) {
    // Check for specific error message from backend first
    const errorData = error?.data || error?.response?.data || {}
    const errorMessage = errorData?.error || errorData?.message
    const hintMessage = errorData?.hint || errorData?.helpful_message
    
    if (errorMessage) {
      return {
        message: errorMessage,
        hint: hintMessage || 'لطفاً اطلاعات را بررسی کنید و دوباره تلاش کنید.',
        type: 'validation',
        recoverable: true,
        action: 'retry'
      }
    }
    
    // Generic 404 for actual page not found
    return {
      message: 'صفحه مورد نظر یافت نشد',
      hint: 'لطفاً آدرس را بررسی کنید و دوباره تلاش کنید.',
      type: 'server',
      recoverable: true,
      action: 'retry'
    }
  }

  // 500 Internal Server Error
  if (status === 500) {
    return {
      message: 'مشکلی در سیستم پیش آمده است',
      hint: 'لطفاً چند دقیقه دیگر دوباره تلاش کنید. اگر مشکل ادامه داشت، با پشتیبانی تماس بگیرید.',
      type: 'server',
      recoverable: true,
      action: 'retry'
    }
  }

  // 503 Service Unavailable
  if (status === 503) {
    return {
      message: 'سرویس در حال حاضر در دسترس نیست',
      hint: 'لطفاً چند دقیقه دیگر دوباره تلاش کنید.',
      type: 'server',
      recoverable: true,
      action: 'retry'
    }
  }

  // Check for specific error messages from backend
  const errorMessage = error?.data?.error || error?.response?.data?.error || error?.message

  if (errorMessage) {
    // Account blocked messages
    if (errorMessage.includes('مسدود') || errorMessage.includes('blocked')) {
      return {
        message: errorMessage,
        hint: 'برای رفع مشکل با پشتیبانی تماس بگیرید.',
        type: 'blocked',
        recoverable: false,
        action: 'contact_support'
      }
    }

    // Invalid credentials messages
    if (errorMessage.includes('اشتباه') || errorMessage.includes('Invalid') || errorMessage.includes('credentials')) {
      return {
        message: errorMessage,
        hint: 'اگر رمز عبور خود را فراموش کرده‌اید، می‌توانید آن را بازیابی کنید.',
        type: 'credentials',
        recoverable: true,
        action: 'forgot_password'
      }
    }

    // Username already exists
    if (errorMessage.includes('قبلاً ثبت شده') || errorMessage.includes('already exists') || errorMessage.includes('already registered')) {
      return {
        message: errorMessage,
        hint: 'اگر قبلاً ثبت‌نام کرده‌اید، وارد حساب کاربری خود شوید.',
        type: 'validation',
        field: 'username',
        recoverable: true,
        action: 'login'
      }
    }

    // Mobile number format errors
    if (errorMessage.includes('موبایل') || errorMessage.includes('mobile') || errorMessage.includes('شماره')) {
      return {
        message: errorMessage,
        hint: 'شماره موبایل باید ۱۱ رقم باشد و با ۰۹ شروع شود (مثال: 09123456789)',
        type: 'validation',
        field: 'username',
        recoverable: true
      }
    }

    // Password errors
    if (errorMessage.includes('رمز عبور') || errorMessage.includes('password')) {
      return {
        message: errorMessage,
        hint: 'رمز عبور باید حداقل ۶ کاراکتر باشد.',
        type: 'validation',
        field: 'password',
        recoverable: true
      }
    }

    // Generic error with message
    return {
      message: errorMessage,
      hint: 'لطفاً اطلاعات را بررسی کنید و دوباره تلاش کنید.',
      type: 'validation',
      recoverable: true
    }
  }

  // Unknown error
  return {
    message: 'خطایی رخ داده است',
    hint: 'لطفاً دوباره تلاش کنید. اگر مشکل ادامه داشت، با پشتیبانی تماس بگیرید.',
    type: 'unknown',
    recoverable: true,
    action: 'retry'
  }
}

/**
 * Get error icon based on error type
 */
export function getErrorIcon(errorType: AuthError['type']): string {
  switch (errorType) {
    case 'network':
      return 'mdi-wifi-off'
    case 'credentials':
      return 'mdi-alert-circle'
    case 'validation':
      return 'mdi-alert'
    case 'blocked':
      return 'mdi-account-cancel'
    case 'server':
      return 'mdi-server-network-off'
    default:
      return 'mdi-alert-circle-outline'
  }
}

/**
 * Get error color based on error type
 */
export function getErrorColor(errorType: AuthError['type']): string {
  switch (errorType) {
    case 'network':
      return 'warning'
    case 'credentials':
      return 'error'
    case 'validation':
      return 'warning'
    case 'blocked':
      return 'error'
    case 'server':
      return 'error'
    default:
      return 'error'
  }
}













