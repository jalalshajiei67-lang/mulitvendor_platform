# OTP System - Local Testing Guide

This guide provides step-by-step instructions for testing the OTP system in your local development environment.

## Prerequisites

- Django backend running
- Nuxt.js frontend running
- Database migrations applied
- A user account with a phone number

## Step 1: Run Database Migrations

First, ensure the OTP model is created in your database:

```bash
# Navigate to Django project directory
cd multivendor_platform/multivendor_platform

# Create migration for OTP model
python manage.py makemigrations users

# Apply migration
python manage.py migrate
```

**Expected Output:**
```
Migrations for 'users':
  users/migrations/0008_otp.py
    - Create model OTP
```

## Step 2: Start Development Servers

### Backend (Django)

```bash
# From multivendor_platform/multivendor_platform directory
python manage.py runserver
```

**Expected:** Server running on `http://localhost:8000`

### Frontend (Nuxt.js)

```bash
# From front_end/nuxt directory
npm run dev
```

**Expected:** Server running on `http://localhost:3000`

## Step 3: Verify OTP Configuration

Check that the OTP system is configured for local development:

1. Open `multivendor_platform/multivendor_platform/settings.py`
2. Verify these settings exist:
   ```python
   OTP_SENDER_CLASS = 'users.services.otp_senders.LocalOTPSender'
   OTP_EXPIRATION_MINUTES = 5
   OTP_RATE_LIMIT_REQUESTS = 3
   OTP_RATE_LIMIT_WINDOW_MINUTES = 15
   ```

## Step 4: Test OTP Login Flow

### 4.1 Access Login Page

1. Open browser: `http://localhost:3000/login`
2. You should see two tabs/buttons:
   - **رمز عبور** (Password)
   - **کد تأیید** (OTP)

### 4.2 Request OTP

1. Click on **کد تأیید** (OTP) button
2. Enter a phone number (Iranian format): `09123456789`
3. Click **ارسال کد تأیید** (Send OTP Code)

**What to Expect:**
- ✅ Success message: "کد تأیید ارسال شد"
- ✅ OTP verification component appears
- ✅ **In Local Mode:** You'll see an info alert with the actual OTP code (e.g., "کد تأیید: 123456")
- ✅ Check your terminal/console where Django is running - you should see:
  ```
  ============================================================
  OTP CODE: 123456
  Recipient: 09123456789
  Purpose: login
  ============================================================
  ```

### 4.3 Verify OTP

1. Enter the 6-digit OTP code shown in the alert or terminal
2. The code should auto-fill if you're in development mode
3. Click **تأیید** (Verify)

**What to Expect:**
- ✅ Successful login
- ✅ Redirect to dashboard
- ✅ User session created

### 4.4 Test Auto-Fill (Development Mode)

In development mode, the OTP code should automatically fill in the input fields. If it doesn't:
1. Check browser console for errors
2. Verify the OTP code is returned in the API response
3. Manually enter the code from the terminal/alert

## Step 5: Test OTP Password Reset Flow

### 5.1 Access Password Reset Page

1. Navigate to: `http://localhost:3000/password-reset`
2. Or click "بازیابی رمز عبور" (Forgot Password) link from login page

### 5.2 Request OTP for Password Reset

1. Enter phone number: `09123456789`
2. Click **ارسال کد تأیید** (Send OTP Code)

**What to Expect:**
- ✅ OTP verification component appears
- ✅ OTP code displayed in alert/terminal

### 5.3 Verify OTP

1. Enter the OTP code
2. Click **تأیید** (Verify)

**What to Expect:**
- ✅ Step 3 appears: "Set New Password"
- ✅ Password form displayed

### 5.4 Set New Password

1. Enter new password (minimum 6 characters)
2. Confirm password
3. Click **تغییر رمز عبور** (Change Password)

**Note:** Password reset endpoint needs to be implemented in backend (currently placeholder)

## Step 6: Test Error Scenarios

### 6.1 Invalid Phone Number

1. Try entering invalid phone: `12345`
2. **Expected:** Validation error message

### 6.2 Wrong OTP Code

1. Request OTP
2. Enter wrong code: `000000`
3. **Expected:** Error message "کد تأیید نامعتبر است"

### 6.3 Expired OTP

1. Request OTP
2. Wait 5+ minutes (or manually expire in database)
3. Try to verify
4. **Expected:** Error message "کد تأیید منقضی شده است"

### 6.4 Rate Limiting

1. Request OTP 4 times within 15 minutes
2. **Expected:** Error on 4th request: "Too many OTP requests. Please wait 15 minutes."

## Step 7: Test API Endpoints Directly

### 7.1 Request OTP via API

```bash
curl -X POST http://localhost:8000/api/auth/otp/request/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "09123456789",
    "purpose": "login"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "کد تأیید برای تست (حالت توسعه)",
  "otp_code": "123456",
  "delivery_method": "local"
}
```

### 7.2 Verify OTP via API

```bash
curl -X POST http://localhost:8000/api/auth/otp/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "09123456789",
    "code": "123456",
    "purpose": "login"
  }'
```

**Expected Response (for login):**
```json
{
  "success": true,
  "message": "کد تأیید صحیح است",
  "token": "your-auth-token-here",
  "user": {
    "id": 1,
    "username": "09123456789",
    ...
  }
}
```

## Step 8: Check Database

Verify OTP records are being created:

```bash
# Access Django shell
python manage.py shell
```

```python
from users.models import OTP

# View recent OTPs
otps = OTP.objects.all().order_by('-created_at')[:5]
for otp in otps:
    print(f"Phone: {otp.phone}, Code: {otp.code}, Purpose: {otp.purpose}, Used: {otp.is_used}, Expires: {otp.expires_at}")

# Check specific OTP
otp = OTP.objects.filter(phone='09123456789', purpose='login').first()
if otp:
    print(f"Code: {otp.code}, Expired: {otp.is_expired()}, Used: {otp.is_used}")
```

## Step 9: Test with Existing User

### 9.1 Using Username Instead of Phone

1. On login page, select OTP method
2. Enter username (phone number) of existing user
3. Request OTP
4. **Expected:** OTP sent to user's phone number from profile

### 9.2 Verify User Login

1. Complete OTP verification
2. **Expected:** Logged in as that user
3. Check user session and token

## Step 10: Monitor Logs

### Backend Logs

Watch Django terminal for:
- OTP generation logs
- OTP verification logs
- Rate limiting messages
- Error messages

### Frontend Logs

Open browser DevTools (F12):
- Console tab: Check for JavaScript errors
- Network tab: Monitor API requests/responses

## Troubleshooting

### Issue: OTP not appearing in alert

**Solution:**
- Check browser console for errors
- Verify API response includes `otp_code` field
- Check Django terminal for OTP code

### Issue: "Too many requests" error

**Solution:**
- Wait 15 minutes, or
- Clear OTP records from database:
  ```python
  from users.models import OTP
  OTP.objects.filter(phone='09123456789').delete()
  ```

### Issue: OTP verification fails

**Solution:**
- Verify code is correct (check terminal/alert)
- Check if OTP is expired (5 minutes)
- Check if OTP was already used
- Verify phone number matches exactly

### Issue: User not found

**Solution:**
- Ensure user exists in database
- Verify phone number format matches user's phone
- Check if using username instead of phone

### Issue: Migration errors

**Solution:**
```bash
# Check migration status
python manage.py showmigrations users

# If needed, fake migration
python manage.py migrate users --fake

# Or reset migrations (careful - data loss)
python manage.py migrate users zero
python manage.py migrate users
```

## Quick Test Checklist

- [ ] Migrations applied successfully
- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 3000)
- [ ] Can access login page
- [ ] OTP login option visible
- [ ] Can request OTP
- [ ] OTP code appears in alert/terminal
- [ ] Can verify OTP successfully
- [ ] Login works after OTP verification
- [ ] Password reset flow works
- [ ] Error handling works (wrong code, expired, etc.)
- [ ] Rate limiting works
- [ ] Database records created correctly

## Next Steps

Once local testing is complete:
1. Test with different phone numbers
2. Test with different purposes (login, password_reset)
3. Test edge cases (expired codes, used codes, etc.)
4. Prepare for Phase 3: SMS integration

## Notes

- **Local Mode:** OTP codes are returned in API response and logged to console
- **No SMS Costs:** In local mode, no actual SMS is sent
- **Auto-Fill:** In development, OTP codes auto-fill for convenience
- **Rate Limiting:** 3 requests per 15 minutes per phone number
- **Expiration:** OTP codes expire after 5 minutes
- **Single Use:** Each OTP code can only be used once

