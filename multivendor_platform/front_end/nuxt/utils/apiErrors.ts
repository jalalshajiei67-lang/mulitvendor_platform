/**
 * API Error Handling Utilities
 * Provides functions to parse and format API error responses
 */

export interface ApiError {
  message: string
  fields?: Record<string, string[]>
  nonFieldErrors?: string[]
}

/**
 * Parse Django REST Framework error response
 * @param error Error object from fetch/axios
 * @returns Formatted error object
 */
export function parseApiError(error: any): ApiError {
  const result: ApiError = {
    message: 'خطای ناشناخته رخ داد',
    fields: {},
    nonFieldErrors: []
  }

  // Check if error has data property (from $fetch)
  const errorData = error?.data || error?.response?.data || error

  if (!errorData) {
    result.message = error?.message || 'خطا در ارتباط با سرور'
    return result
  }

  // Handle simple detail message
  if (typeof errorData.detail === 'string') {
    result.message = errorData.detail
    return result
  }

  // Handle non-field errors
  if (errorData.non_field_errors) {
    result.nonFieldErrors = Array.isArray(errorData.non_field_errors)
      ? errorData.non_field_errors
      : [String(errorData.non_field_errors)]
  }

  // Parse field-specific errors
  const fieldErrors: Record<string, string[]> = {}
  let hasFieldErrors = false

  for (const [key, value] of Object.entries(errorData)) {
    if (key === 'detail' || key === 'non_field_errors') {
      continue
    }

    if (Array.isArray(value)) {
      fieldErrors[key] = value.map(String)
      hasFieldErrors = true
    } else if (typeof value === 'string') {
      fieldErrors[key] = [value]
      hasFieldErrors = true
    } else if (typeof value === 'object' && value !== null) {
      // Handle nested errors
      fieldErrors[key] = [JSON.stringify(value)]
      hasFieldErrors = true
    }
  }

  if (hasFieldErrors) {
    result.fields = fieldErrors
  }

  // Generate a comprehensive error message
  if (result.nonFieldErrors.length > 0) {
    result.message = result.nonFieldErrors.join('. ')
  } else if (hasFieldErrors) {
    result.message = 'لطفاً خطاهای فرم را بررسی کنید'
  }

  return result
}

/**
 * Format API error for display in a snackbar or alert
 * @param error Error object from fetch/axios
 * @returns User-friendly error message
 */
export function formatErrorMessage(error: any): string {
  const parsed = parseApiError(error)
  
  // If we have field errors, create a detailed message
  if (parsed.fields && Object.keys(parsed.fields).length > 0) {
    const fieldMessages: string[] = []
    
    for (const [field, messages] of Object.entries(parsed.fields)) {
      const fieldLabel = getFieldLabel(field)
      fieldMessages.push(`${fieldLabel}: ${messages.join(', ')}`)
    }
    
    return fieldMessages.join('\n')
  }
  
  return parsed.message
}

/**
 * Get Persian label for field name
 * @param fieldName Field name from API
 * @returns Persian label
 */
function getFieldLabel(fieldName: string): string {
  const fieldLabels: Record<string, string> = {
    name: 'نام محصول',
    description: 'توضیحات',
    price: 'قیمت',
    stock: 'موجودی',
    vendor: 'فروشنده',
    subcategories: 'زیردسته',
    primary_category: 'دسته اصلی',
    image: 'تصویر',
    images: 'تصاویر',
    slug: 'نامک (Slug)',
    is_active: 'وضعیت',
    meta_title: 'عنوان متا',
    meta_description: 'توضیحات متا',
    canonical_url: 'URL کانونیکال',
    schema_markup: 'Schema Markup',
    image_alt_text: 'متن جایگزین تصویر',
    og_image: 'تصویر Open Graph'
  }
  
  return fieldLabels[fieldName] || fieldName
}

/**
 * Create a formatted error list for display
 * @param error Error object from fetch/axios
 * @returns Array of error messages
 */
export function getErrorList(error: any): string[] {
  const parsed = parseApiError(error)
  const errors: string[] = []
  
  // Add non-field errors
  if (parsed.nonFieldErrors && parsed.nonFieldErrors.length > 0) {
    errors.push(...parsed.nonFieldErrors)
  }
  
  // Add field errors
  if (parsed.fields && Object.keys(parsed.fields).length > 0) {
    for (const [field, messages] of Object.entries(parsed.fields)) {
      const fieldLabel = getFieldLabel(field)
      messages.forEach(msg => {
        errors.push(`${fieldLabel}: ${msg}`)
      })
    }
  }
  
  // If no specific errors, add the general message
  if (errors.length === 0) {
    errors.push(parsed.message)
  }
  
  return errors
}

/**
 * Check if error is a validation error (400 Bad Request)
 * @param error Error object
 * @returns True if validation error
 */
export function isValidationError(error: any): boolean {
  const status = error?.status || error?.response?.status || error?.statusCode
  return status === 400
}

/**
 * Check if error is an authentication error (401 Unauthorized)
 * @param error Error object
 * @returns True if auth error
 */
export function isAuthError(error: any): boolean {
  const status = error?.status || error?.response?.status || error?.statusCode
  return status === 401
}

/**
 * Check if error is a permission error (403 Forbidden)
 * @param error Error object
 * @returns True if permission error
 */
export function isPermissionError(error: any): boolean {
  const status = error?.status || error?.response?.status || error?.statusCode
  return status === 403
}

/**
 * Check if error is a not found error (404)
 * @param error Error object
 * @returns True if not found error
 */
export function isNotFoundError(error: any): boolean {
  const status = error?.status || error?.response?.status || error?.statusCode
  return status === 404
}






