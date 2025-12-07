# Testing Guide: Product Creation Error Handling

## Overview
This guide helps you test the improved error handling for product creation.

## Prerequisites
1. Backend server running (Django)
2. Frontend server running (Nuxt)
3. User logged in as a supplier/vendor

## Test Scenarios

### Test 1: Empty Product Name
**Steps:**
1. Navigate to Supplier Dashboard → Products
2. Click "افزودن محصول جدید" (Add New Product)
3. Leave the "نام محصول" field empty
4. Fill in other required fields (description, price, stock)
5. Click save

**Expected Result:**
- Form validation should prevent submission
- Error message: "نام محصول الزامی است"

---

### Test 2: Short Product Name
**Steps:**
1. Start adding a new product
2. Enter "ab" in the name field (less than 3 characters)
3. Fill in other fields
4. Click save

**Expected Result:**
- Backend validation should reject it
- Error snackbar shows: "نام محصول: نام محصول باید حداقل ۳ کاراکتر باشد"

---

### Test 3: Empty Description
**Steps:**
1. Start adding a new product
2. Enter a valid name
3. Leave description empty OR enter only HTML tags with no text
4. Fill in price and stock
5. Click save

**Expected Result:**
- Form validation or backend validation should reject it
- Error message: "توضیحات نمی‌تواند خالی باشد"

---

### Test 4: Short Description
**Steps:**
1. Start adding a new product
2. Enter a valid name
3. Enter less than 10 characters in description (e.g., "test")
4. Fill in price and stock
5. Click save

**Expected Result:**
- Backend validation should reject it
- Error message: "توضیحات: توضیحات باید حداقل ۱۰ کاراکتر باشد"

---

### Test 5: Zero Price
**Steps:**
1. Start adding a new product
2. Fill in name and description
3. Set price to 0
4. Set stock to any positive number
5. Click save

**Expected Result:**
- Backend validation should reject it
- Error message: "قیمت: قیمت نمی‌تواند صفر باشد"

---

### Test 6: Negative Price
**Steps:**
1. Start adding a new product
2. Fill in name and description
3. Set price to -1000 or any negative number
4. Set stock to any positive number
5. Click save

**Expected Result:**
- Frontend validation should prevent it (if number field restricts it)
- Or backend validation rejects with: "قیمت: قیمت نمی‌تواند منفی باشد"

---

### Test 7: Negative Stock
**Steps:**
1. Start adding a new product
2. Fill in name, description, and valid price
3. Set stock to -5 or any negative number
4. Click save

**Expected Result:**
- Frontend validation should prevent it (if number field restricts it)
- Or backend validation rejects with: "موجودی: موجودی نمی‌تواند منفی باشد"

---

### Test 8: Multiple Validation Errors
**Steps:**
1. Start adding a new product
2. Enter "ab" as name (too short)
3. Enter "test" as description (too short)
4. Set price to 0
5. Click save

**Expected Result:**
- Error snackbar displays all errors in separate lines:
  ```
  نام محصول: نام محصول باید حداقل ۳ کاراکتر باشد
  توضیحات: توضیحات باید حداقل ۱۰ کاراکتر باشد
  قیمت: قیمت نمی‌تواند صفر باشد
  ```

---

### Test 9: Too Many Images
**Steps:**
1. Start adding a new product
2. Fill in all required fields correctly
3. Try to upload more than 20 images
4. Click save

**Expected Result:**
- Error message: "تصاویر: حداکثر ۲۰ تصویر برای هر محصول مجاز است"

---

### Test 10: Successful Creation
**Steps:**
1. Start adding a new product
2. Enter valid name (e.g., "لپ تاپ ایسوس ROG")
3. Enter valid description (at least 10 characters with meaningful content)
4. Set price to a positive number (e.g., 45000000)
5. Set stock to a positive number (e.g., 5)
6. Optionally upload 1-20 images
7. Select a subcategory
8. Click save

**Expected Result:**
- Success snackbar appears: "محصول '[product-name]' با موفقیت ایجاد شد!"
- Redirect to products list after 1.5 seconds
- Product appears in the list

---

## Manual API Testing with curl

### Test Empty Name
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "",
    "description": "Test description with enough characters",
    "price": 100000,
    "stock": 10
  }'
```

**Expected Response:**
```json
{
  "name": ["نام محصول نمی‌تواند خالی باشد"]
}
```

### Test Short Name
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ab",
    "description": "Test description with enough characters",
    "price": 100000,
    "stock": 10
  }'
```

**Expected Response:**
```json
{
  "name": ["نام محصول باید حداقل ۳ کاراکتر باشد"]
}
```

### Test Zero Price
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Valid Product Name",
    "description": "Test description with enough characters",
    "price": 0,
    "stock": 10
  }'
```

**Expected Response:**
```json
{
  "price": ["قیمت نمی‌تواند صفر باشد"]
}
```

### Test Multiple Errors
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ab",
    "description": "short",
    "price": 0,
    "stock": -5
  }'
```

**Expected Response:**
```json
{
  "name": ["نام محصول باید حداقل ۳ کاراکتر باشد"],
  "description": ["توضیحات باید حداقل ۱۰ کاراکتر باشد"],
  "price": ["قیمت نمی‌تواند صفر باشد"],
  "stock": ["موجودی نمی‌تواند منفی باشد"]
}
```

---

## Browser Console Testing

Open browser console (F12) and run:

```javascript
// Test with fetch API
fetch('http://localhost:8000/api/products/', {
  method: 'POST',
  headers: {
    'Authorization': 'Token YOUR_AUTH_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'ab',
    description: 'short',
    price: 0,
    stock: 10
  })
})
.then(r => r.json())
.then(console.log)
.catch(console.error)
```

---

## Checklist

- [ ] Test 1: Empty Product Name
- [ ] Test 2: Short Product Name  
- [ ] Test 3: Empty Description
- [ ] Test 4: Short Description
- [ ] Test 5: Zero Price
- [ ] Test 6: Negative Price
- [ ] Test 7: Negative Stock
- [ ] Test 8: Multiple Validation Errors
- [ ] Test 9: Too Many Images
- [ ] Test 10: Successful Creation

---

## Notes

1. **Error Snackbar**: Appears at the top of the screen for 8 seconds
2. **Multi-line Errors**: Multiple errors are displayed on separate lines
3. **Close Button**: Snackbar includes a "بستن" (Close) button
4. **Console Logging**: Check browser console for detailed error objects
5. **Backend Logs**: Check Django server logs for validation errors

---

## Troubleshooting

### Error snackbar not showing
- Check browser console for JavaScript errors
- Ensure `showErrorSnackbar` state is being set to true
- Verify snackbar component is present in the template

### Errors not being formatted
- Check that `apiErrors.ts` utility is being imported correctly
- Verify the error object has the expected structure (`error.data`)
- Check that `formatErrorMessage()` is being called

### Backend returning 500 instead of 400
- Check Django server logs for Python exceptions
- Verify serializer validation is working correctly
- Ensure database constraints are not causing issues

### Persian messages not showing
- Verify `extra_kwargs` are set correctly in serializer
- Check that validation methods return Persian error messages
- Ensure Django is using UTF-8 encoding

---

## Success Criteria

✅ All validation errors display in Persian
✅ Field-specific errors show which field has the issue
✅ Multiple errors are all shown together
✅ Error messages are clear and actionable
✅ Snackbar is easy to read with proper formatting
✅ Users can easily close the error message
✅ Console logs provide detailed error information for debugging








