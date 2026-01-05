# Testing Kavenegar OTP API Locally

This guide helps you test the Kavenegar OTP API integration locally before deploying to production.

## Quick Test Script

We have a test script that will help you debug the Kavenegar API integration.

### Step 1: Set Environment Variables

Before running the test, you need to set the environment variables:

```bash
# In your terminal (Fish shell)
set -x KAVENEGAR_API_KEY "7653646D726D375276504E3875306D61374C7379464C73472B6D496570774C7134586B307A3556307A496B3D"
set -x KAVENEGAR_OTP_TEMPLATE_NAME "OTPInedexo"
set -x OTP_SENDER_CLASS "users.services.otp_senders.KavenegarOTPSender"
```

Or for Bash/Zsh:
```bash
export KAVENEGAR_API_KEY="7653646D726D375276504E3875306D61374C7379464C73472B6D496570774C7134586B307A3556307A496B3D"
export KAVENEGAR_OTP_TEMPLATE_NAME="OTPInedexo"
export OTP_SENDER_CLASS="users.services.otp_senders.KavenegarOTPSender"
```

### Step 2: Run the Test Script

```bash
# Navigate to Django project directory
cd multivendor_platform/multivendor_platform

# Run the test script
python test_kavenegar_otp.py [phone_number]

# Or with phone number as argument
python test_kavenegar_otp.py 09123456789
```

### Step 3: What the Script Tests

The script will:
1. ✅ Check if environment variables are set correctly
2. ✅ Test the Kavenegar API directly with a test code
3. ✅ Test using the OTP Sender class
4. ✅ Show detailed error messages if something fails

## Manual Testing via Django Shell

You can also test manually using Django shell:

### Step 1: Start Django Shell

```bash
cd multivendor_platform/multivendor_platform
python manage.py shell
```

### Step 2: Test Configuration

```python
from django.conf import settings

# Check if settings are loaded
print(f"API Key: {settings.KAVENEGAR_API_KEY[:10]}..." if settings.KAVENEGAR_API_KEY else "NOT SET")
print(f"Template: {settings.KAVENEGAR_OTP_TEMPLATE_NAME}")
print(f"Sender Class: {settings.OTP_SENDER_CLASS}")
```

### Step 3: Test OTP Sender

```python
from users.services.otp_senders import KavenegarOTPSender

# Create sender instance
sender = KavenegarOTPSender()

# Test sending OTP
result = sender.send_otp("123456", "09123456789", "login")
print(result)
```

### Step 4: Test Full OTP Service

```python
from users.services.otp_service import OTPService

# Create service instance
service = OTPService()

# Generate and send OTP
result = service.generate_otp("09123456789", "login")
print(result)
```

## Testing via API Endpoint

### Step 1: Start Django Server

```bash
cd multivendor_platform/multivendor_platform

# Make sure environment variables are set first!
python manage.py runserver
```

### Step 2: Test OTP Request Endpoint

```bash
curl -X POST http://localhost:8000/api/auth/otp/request/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "09123456789",
    "purpose": "login"
  }'
```

**Expected Response (Success):**
```json
{
  "success": true,
  "message": "کد تأیید با موفقیت ارسال شد",
  "otp_id": 1,
  "delivery_method": "kavenegar"
}
```

**Expected Response (Error):**
```json
{
  "error": "...",
  "helpful_message": "..."
}
```

### Step 3: Check Django Logs

Watch the terminal where Django is running for:
- ✅ Success: `OTP sent successfully via Kavenegar to 09123456789`
- ❌ Errors: Any error messages from Kavenegar API

## Common Issues & Solutions

### Issue 1: API Key Not Set

**Error:** `KAVENEGAR_API_KEY not configured in settings`

**Solution:**
```bash
# Make sure you set the environment variable BEFORE starting Django
export KAVENEGAR_API_KEY="your-api-key"
python manage.py runserver
```

### Issue 2: Template Name Not Set

**Error:** `KAVENEGAR_OTP_TEMPLATE_NAME not configured in settings`

**Solution:**
```bash
export KAVENEGAR_OTP_TEMPLATE_NAME="OTPInedexo"
```

### Issue 3: Wrong Sender Class

**Error:** OTP codes appear in console instead of SMS

**Solution:**
```bash
export OTP_SENDER_CLASS="users.services.otp_senders.KavenegarOTPSender"
# Restart Django server
```

### Issue 4: API Returns Error

**Error:** Kavenegar API returns error status

**Check:**
1. ✅ API key is correct in Kavenegar panel
2. ✅ Template name matches exactly (case-sensitive)
3. ✅ Template is active/approved in Kavenegar panel
4. ✅ Template accepts 1 token parameter
5. ✅ Account has sufficient credit
6. ✅ Phone number format is correct (09XXXXXXXXX)

### Issue 5: Network/Connection Error

**Error:** `Connection error` or `Timeout`

**Check:**
1. ✅ Internet connection is working
2. ✅ Kavenegar API is accessible (not blocked)
3. ✅ Firewall allows outbound HTTPS connections

## Debugging Steps

### Step 1: Verify Settings

```bash
python manage.py shell
```

```python
from django.conf import settings
print("API Key:", settings.KAVENEGAR_API_KEY)
print("Template:", settings.KAVENEGAR_OTP_TEMPLATE_NAME)
print("Sender:", settings.OTP_SENDER_CLASS)
```

### Step 2: Test API Directly

Use the test script:
```bash
python test_kavenegar_otp.py 09123456789
```

### Step 3: Check Kavenegar Panel

1. Log in to Kavenegar panel
2. Check API key is correct
3. Verify template `OTPInedexo` exists and is active
4. Check account balance
5. View API logs/requests

### Step 4: Check Django Logs

Enable debug logging in `settings.py`:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'users.services.otp_senders': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Production Checklist

Before deploying to production:

- [ ] API key is set in CapRover environment variables
- [ ] Template name is set correctly
- [ ] OTP_SENDER_CLASS is set to KavenegarOTPSender
- [ ] Tested locally and working
- [ ] Kavenegar template is approved/active
- [ ] Account has sufficient credit
- [ ] Phone number normalization works correctly

## Quick Reference

### Environment Variables (Local)

```bash
export KAVENEGAR_API_KEY="your-api-key"
export KAVENEGAR_OTP_TEMPLATE_NAME="OTPInedexo"
export OTP_SENDER_CLASS="users.services.otp_senders.KavenegarOTPSender"
```

### Environment Variables (Production - CapRover)

In CapRover → Apps → multivendor-backend → App Configs:
```
KAVENEGAR_API_KEY=your-api-key
KAVENEGAR_OTP_TEMPLATE_NAME=OTPInedexo
OTP_SENDER_CLASS=users.services.otp_senders.KavenegarOTPSender
```

### Test Command

```bash
cd multivendor_platform/multivendor_platform
python test_kavenegar_otp.py 09123456789
```

### API Test

```bash
curl -X POST http://localhost:8000/api/auth/otp/request/ \
  -H "Content-Type: application/json" \
  -d '{"phone": "09123456789", "purpose": "login"}'
```




