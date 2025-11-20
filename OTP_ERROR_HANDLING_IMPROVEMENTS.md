# OTP System - Error Handling Improvements

## Overview
All error messages have been optimized for Persian language and non-technical users over 40 years old. Messages are clear, friendly, helpful, and avoid technical jargon.

## Error Message Principles

1. **Clear and Simple**: Use everyday language, avoid technical terms
2. **Helpful**: Provide actionable guidance on what to do next
3. **Friendly**: Use respectful and polite tone
4. **Persian Language**: All messages in Farsi/Persian
5. **Context-Aware**: Explain why the error occurred when helpful

## Backend Error Messages

### Rate Limiting
**Before:** "Too many OTP requests. Please wait 15 minutes."

**After:** 
```
"شما در 15 دقیقه گذشته 3 بار کد درخواست کرده‌اید. 
لطفاً 15 دقیقه صبر کنید و سپس دوباره تلاش کنید. 
این محدودیت برای امنیت حساب شما اعمال شده است."
```

### Invalid OTP Code
**Before:** "کد تأیید نامعتبر است"

**After:**
```
"کد وارد شده صحیح نیست. لطفاً دقت کنید و کد 6 رقمی را به درستی وارد کنید. 
اگر کد را دریافت نکرده‌اید، می‌توانید دکمه 'ارسال مجدد کد' را بزنید."
```

### Expired OTP
**Before:** "کد تأیید منقضی شده است. لطفاً کد جدیدی درخواست کنید"

**After:**
```
"متأسفانه کد تأیید شما منقضی شده است. کدهای تأیید فقط 5 دقیقه اعتبار دارند. 
لطفاً دکمه 'ارسال مجدد کد' را بزنید تا کد جدیدی برای شما ارسال شود."
```

### Max Attempts Exceeded
**Before:** "تعداد تلاش‌های مجاز برای این کد به پایان رسیده است. لطفاً کد جدیدی درخواست کنید"

**After:**
```
"شما بیش از حد مجاز برای وارد کردن کد تلاش کرده‌اید. 
برای امنیت حساب شما، این کد دیگر قابل استفاده نیست. 
لطفاً دکمه 'ارسال مجدد کد' را بزنید تا کد جدیدی دریافت کنید."
```

### User Not Found
**Before:** "کاربری با این نام کاربری یافت نشد"

**After:**
```
"شماره موبایل وارد شده در سیستم ثبت نشده است. 
لطفاً شماره موبایل خود را بررسی کنید. 
اگر حساب کاربری ندارید، می‌توانید از صفحه ثبت‌نام استفاده کنید."
```

### Server Errors
**Before:** "خطا در ارسال کد تأیید. لطفاً دوباره تلاش کنید."

**After:**
```
"متأسفانه در ارسال کد تأیید مشکلی پیش آمده است.
لطفاً چند لحظه صبر کنید و دوباره تلاش کنید. 
اگر مشکل ادامه داشت، با پشتیبانی تماس بگیرید."
```

## Frontend Validation Messages

### Phone Number Validation
**Before:** "شماره موبایل معتبر نیست (مثال: 09123456789)"

**After:** "شماره موبایل باید 11 رقم و با 09 شروع شود. مثال: 09123456789"

### OTP Code Validation
**Before:** "کد تأیید باید 6 رقم باشد"

**After:** 
```
"کد تأیید باید دقیقاً 6 رقم باشد. شما X رقم وارد کرده‌اید. 
لطفاً کد 6 رقمی را کامل وارد کنید."
```

### Password Validation
**Before:** "رمز عبور باید حداقل ۶ کاراکتر باشد"

**After:** "رمز عبور باید حداقل ۶ کاراکتر باشد. لطفاً رمز عبور قوی‌تری انتخاب کنید"

## Error Display Improvements

### Visual Enhancements
- Added error icons (mdi-alert-circle) for better visibility
- Improved typography with clear hierarchy
- Separated main error message from helpful hints
- Better spacing and readability

### Error Message Structure
```
[Main Error Message - Bold, Larger Font]
[Helpful Hint/Next Steps - Smaller, Lighter Font]
```

### Example Error Display
```
⚠️ کد وارد شده صحیح نیست. لطفاً دقت کنید و کد 6 رقمی را به درستی وارد کنید.

اگر کد را دریافت نکرده‌اید، می‌توانید دکمه 'ارسال مجدد کد' را بزنید.
```

## User Experience Improvements

1. **Clear Instructions**: Every error tells users what to do next
2. **No Technical Jargon**: Avoided terms like "API", "endpoint", "validation"
3. **Empathetic Tone**: Used phrases like "متأسفانه" (unfortunately) to show understanding
4. **Security Explanations**: Explained why limitations exist (e.g., "برای امنیت حساب شما")
5. **Alternative Actions**: Always provide next steps (e.g., "می‌توانید کد جدیدی درخواست کنید")

## Testing Error Scenarios

### Test Cases for Error Messages

1. **Invalid Phone Number**
   - Enter: `12345`
   - Expected: Clear message about 11 digits starting with 09

2. **Wrong OTP Code**
   - Enter wrong code
   - Expected: Friendly message with suggestion to resend

3. **Expired OTP**
   - Wait 5+ minutes, then verify
   - Expected: Explanation of expiration with resend option

4. **Rate Limiting**
   - Request OTP 4 times quickly
   - Expected: Clear explanation of limit and wait time

5. **User Not Found**
   - Enter unregistered phone
   - Expected: Helpful message with registration suggestion

## Implementation Files

### Backend
- `users/services/otp_service.py` - Core error messages
- `users/views.py` - API endpoint error responses
- `users/serializers.py` - Validation error messages

### Frontend
- `components/auth/OtpVerification.vue` - OTP component errors
- `pages/login.vue` - Login page validation
- `pages/password-reset.vue` - Password reset errors

## Best Practices Applied

1. ✅ All messages in Persian
2. ✅ Simple, everyday language
3. ✅ Actionable guidance
4. ✅ Friendly and respectful tone
5. ✅ No technical jargon
6. ✅ Clear visual hierarchy
7. ✅ Helpful hints and suggestions
8. ✅ Security explanations where needed

