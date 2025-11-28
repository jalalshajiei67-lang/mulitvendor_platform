# Error Handling Improvements for Product Creation

## Overview
This document describes the improvements made to error handling for product creation in the multivendor platform.

## Problem
- Users were seeing vague error messages when product creation failed
- 400 Bad Request errors didn't show specific validation issues
- Frontend only displayed generic "خطا در ذخیره محصول" message
- Django REST Framework validation errors weren't properly parsed

## Solution

### 1. Backend Improvements (`products/serializers.py`)

#### Added Persian Error Messages
```python
extra_kwargs = {
    'name': {
        'required': True,
        'error_messages': {
            'required': 'نام محصول الزامی است',
            'blank': 'نام محصول نمی‌تواند خالی باشد',
            'max_length': 'نام محصول نمی‌تواند بیشتر از ۲۰۰ کاراکتر باشد'
        }
    },
    # ... more fields
}
```

#### Enhanced Field Validation
- `validate_name()`: Ensures name is not empty and at least 3 characters
- `validate_description()`: Validates description has real content (not just HTML tags), minimum 10 characters
- `validate_price()`: Ensures price is positive and not zero
- `validate_stock()`: Ensures stock is non-negative
- `validate()`: General validation for images count, description content

#### Better Error Messages
All validation errors now return structured, Persian messages:
- Field-specific errors: `{"field_name": ["error message in Persian"]}`
- Non-field errors: `{"non_field_errors": ["error message"]}`
- General errors: `{"detail": "error message"}`

### 2. Frontend Improvements

#### New Error Utility (`utils/apiErrors.ts`)
Created a comprehensive error handling utility with functions:

- `parseApiError(error)`: Parses Django REST Framework errors into structured format
- `formatErrorMessage(error)`: Formats errors for display in snackbar/alert
- `getErrorList(error)`: Returns array of all error messages
- `getFieldLabel(fieldName)`: Translates field names to Persian
- Helper functions: `isValidationError()`, `isAuthError()`, `isPermissionError()`, `isNotFoundError()`

#### Updated Components

**ProductForm.vue**
- Improved error snackbar with multi-line support
- Added close button to error snackbar
- Increased timeout to 8 seconds for better readability
- Uses `formatErrorMessage()` to show detailed validation errors

```vue
<v-snackbar
  v-model="showErrorSnackbar"
  color="error"
  :timeout="8000"
  location="top"
  multi-line
>
  <div style="white-space: pre-line; max-width: 600px;">
    {{ errorMessage }}
  </div>
  <template v-slot:actions>
    <v-btn variant="text" @click="showErrorSnackbar = false">
      بستن
    </v-btn>
  </template>
</v-snackbar>
```

**Product Store (`stores/product.ts`)**
- Updated `createProduct()` and `updateProduct()` methods
- Now uses `formatErrorMessage()` for better error messages
- Error state contains user-friendly Persian messages

**Admin Dashboard (`pages/admin/dashboard/products/new.vue`)**
- Updated to use error formatting utility
- Shows detailed validation errors in alert

### 3. Error Message Examples

#### Before
```
Error: 400 Bad Request
خطا در ذخیره محصول
```

#### After
```
نام محصول: نام محصول نمی‌تواند خالی باشد
توضیحات: توضیحات باید حداقل ۱۰ کاراکتر باشد
قیمت: قیمت نمی‌تواند صفر باشد
```

## Field Validations

### Required Fields
- **name** (نام محصول): Required, minimum 3 characters
- **description** (توضیحات): Required, minimum 10 characters of actual content
- **price** (قیمت): Required, must be positive and not zero

### Optional Fields with Validation
- **stock** (موجودی): Must be non-negative if provided
- **subcategories** (زیردسته): At least one recommended
- **images** (تصاویر): Maximum 20 images per product

### Field Labels (Persian)
- name → نام محصول
- description → توضیحات
- price → قیمت
- stock → موجودی
- vendor → فروشنده
- subcategories → زیردسته
- primary_category → دسته اصلی
- image/images → تصویر/تصاویر
- slug → نامک (Slug)
- is_active → وضعیت

## Usage

### Using the Error Utility in Components
```typescript
import { formatErrorMessage, parseApiError, getErrorList } from '~/utils/apiErrors'

try {
  await productApi.createProduct(formData)
} catch (error: any) {
  // Get formatted message for display
  errorMessage.value = formatErrorMessage(error)
  
  // Or get structured error data
  const parsed = parseApiError(error)
  console.log('Fields with errors:', parsed.fields)
  console.log('Non-field errors:', parsed.nonFieldErrors)
  
  // Or get list of all errors
  const errorList = getErrorList(error)
  errorList.forEach(err => console.log(err))
}
```

### Checking Error Types
```typescript
import { isValidationError, isAuthError, isPermissionError } from '~/utils/apiErrors'

try {
  await someApi()
} catch (error) {
  if (isValidationError(error)) {
    // Handle validation errors (400)
  } else if (isAuthError(error)) {
    // Handle auth errors (401)
  } else if (isPermissionError(error)) {
    // Handle permission errors (403)
  }
}
```

## Testing

To test the improved error handling:

### 1. Empty Name
- Leave name field empty
- Expected: "نام محصول الزامی است"

### 2. Short Name
- Enter name with less than 3 characters (e.g., "ab")
- Expected: "نام محصول باید حداقل ۳ کاراکتر باشد"

### 3. Empty Description
- Leave description empty or add only spaces/HTML
- Expected: "توضیحات نمی‌تواند خالی باشد"

### 4. Short Description
- Enter description with less than 10 characters
- Expected: "توضیحات باید حداقل ۱۰ کاراکتر باشد"

### 5. Zero Price
- Set price to 0
- Expected: "قیمت نمی‌تواند صفر باشد"

### 6. Negative Price
- Set price to negative value
- Expected: "قیمت نمی‌تواند منفی باشد"

### 7. Negative Stock
- Set stock to negative value
- Expected: "موجودی نمی‌تواند منفی باشد"

### 8. Too Many Images
- Upload more than 20 images
- Expected: "حداکثر ۲۰ تصویر برای هر محصول مجاز است"

### 9. Multiple Errors
- Submit form with multiple validation errors
- Expected: All errors shown in multi-line format

## Benefits

1. **Better UX**: Users see exactly what's wrong with their input
2. **Persian Messages**: All error messages in Persian for better understanding
3. **Field-Specific**: Errors point to specific fields
4. **Consistent**: Same error handling across all product forms
5. **Maintainable**: Centralized error handling logic
6. **Extensible**: Easy to add new validation rules and messages

## Files Changed

### Backend
- `multivendor_platform/products/serializers.py` - Enhanced validation
- `multivendor_platform/products/views.py` - Better error handling in viewsets

### Frontend
- `front_end/nuxt/utils/apiErrors.ts` - New error utility (Created)
- `front_end/nuxt/components/supplier/ProductForm.vue` - Improved error display
- `front_end/nuxt/stores/product.ts` - Better error messages in store
- `front_end/nuxt/pages/admin/dashboard/products/new.vue` - Use error utility

## Future Improvements

1. Add inline field validation (real-time)
2. Add visual indicators for fields with errors
3. Auto-focus first field with error
4. Add error summary at top of form
5. Add more specific validation rules (e.g., price ranges, name patterns)
6. Add validation for image file types and sizes
7. Implement error recovery suggestions (e.g., "Did you mean...?")





