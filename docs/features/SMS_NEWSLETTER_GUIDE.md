# SMS Newsletter Guide

## Overview

The SMS Newsletter feature allows you to send automated SMS notifications to suppliers when they match customer requirements. The system uses the Kavenegar SMS service provider.

---

## Features

- ✅ Automatic SMS sending to suppliers
- ✅ Template-based messaging
- ✅ Local development mode (logs instead of sending)
- ✅ Production mode (sends real SMS)
- ✅ Persian language support
- ✅ Automatic token truncation to avoid errors
- ✅ Space removal for optimal token length

---

## Setup

### 1. Kavenegar Account Setup

1. **Create Account:** https://panel.kavenegar.com
2. **Get API Key:** 
   - Go to Settings → API
   - Copy your 88-character API key
3. **Create Template:**
   - Go to Settings → Templates
   - Name: `SupplyerNotif`
   - Content:
     ```
     سلام، %token عزیز برای %token2 مشتری جدیدی منتظر شماست.
     ایندکسو
     indexo.ir/s/notif
     ```
4. **Whitelist IP:**
   - Go to Settings → Security → IP Whitelist
   - Add your server IP: `185.208.172.76`
   - Add local IP for testing if needed

### 2. Environment Configuration

Add to your `.env` file:

```bash
# Production
KAVENEGAR_API_KEY=your-88-char-api-key-here
KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME=SupplyerNotif

# Development (optional - for testing without sending SMS)
# SMS_NEWSLETTER_LOCAL_MODE=true
```

### 3. Django Settings

Already configured in `settings.py`:

```python
KAVENEGAR_API_KEY = os.environ.get('KAVENEGAR_API_KEY', '')
KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME = os.environ.get('KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME', 'SupplyerNotif')
SMS_NEWSLETTER_LOCAL_MODE = os.environ.get('SMS_NEWSLETTER_LOCAL_MODE', '').lower() in ('true', '1', 'yes') or not KAVENEGAR_API_KEY
```

---

## Usage

### From Django Admin

1. Go to **SMS Newsletter → Sellers**
2. Add a new seller or select existing one
3. Apply a filter (e.g., filter by working field)
4. SMS will be sent automatically to matching sellers

### Programmatically

```python
from sms_newsletter.models import Seller
from sms_newsletter.services import send_sms_via_kavenegar

# Get seller
seller = Seller.objects.get(mobile_number='09123456789')

# Send SMS
filter_name = 'خط تولید نوار بهداشتی'
result = send_sms_via_kavenegar(seller, filter_name)

if result['success']:
    print("SMS sent successfully!")
else:
    print(f"Error: {result['message']}")
```

### Testing Script

```bash
cd multivendor_platform/multivendor_platform

# Set environment variables
export KAVENEGAR_API_KEY="your-api-key"
export KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME="SupplyerNotif"

# Activate virtual environment
source ../../venv/bin/activate

# Run test
python test_sms_newsletter.py
```

---

## Token Processing

### Why Token Truncation?

Kavenegar API has a limitation: HTTP headers cannot exceed a certain size. Persian characters expand to 9 bytes each when URL-encoded (e.g., `ا` → `%D8%A7`), which quickly exceeds the limit.

### Solution

- **Maximum token length:** 3 characters
- **Space removal:** All spaces are removed before truncation
- **Example:**
  ```
  "رجبعلی طیبی نژاد" → "رجبعلیطیبینژاد" → "رجب" (3 chars)
  "خط تولید نوار" → "خطتولیدنوار" → "خطت" (3 chars)
  ```

### Impact

The SMS will show abbreviated names/filters:

```
Original:
  Name: رجبعلی طیبی نژاد
  Filter: خط تولید نوار بهداشتی صنعتی

SMS Content:
  سلام، رجب عزیز برای خطت مشتری جدیدی منتظر شماست.
  ایندکسو
  indexo.ir/s/notif
```

### Alternative Options

If truncation is not acceptable:

**Option A:** Use generic template without tokens
```
سلام عزیز، یک مشتری جدید منتظر شماست.
ایندکسو
indexo.ir/s/notif
```

**Option B:** Contact Kavenegar support to increase header size limit

---

## Local Development Mode

When `KAVENEGAR_API_KEY` is not set or `SMS_NEWSLETTER_LOCAL_MODE=true`:

- ✅ SMS content is logged to console
- ✅ No real SMS is sent
- ✅ No API calls to Kavenegar
- ✅ Perfect for development/testing

Example output:

```
======================================================================
📱 SUPPLIER NOTIFICATION SMS (LOCAL MODE - NOT SENT)
======================================================================
To: 09124242066
Seller: رجبعلی طیبی نژاد
Filter Name: خطت

Message Template: SupplyerNotif
Token 1 (Name): رجب
Token 2 (Filter): خطت

Full Message:
سلام، رجب عزیز برای خطت مشتری جدیدی منتظر شماست.
ایندکسو
indexo.ir/s/notif
======================================================================
```

---

## Error Handling

### HTTP 431 Error

**Error:** "Request Header Fields Too Large"

**Cause:** 
- Tokens too long
- Spaces in tokens
- Large HTTP headers

**Solution:** 
- ✅ Already implemented: tokens truncated to 3 chars
- ✅ Spaces removed automatically
- ✅ Minimal HTTP headers used

### Invalid Phone Number

**Error:** Validation error in Django admin

**Solution:**
- Ensure phone is in format: `09XXXXXXXXX`
- System accepts: `+98`, `0098`, `98`, `9` prefixes
- Automatically normalized to `09XXXXXXXXX`

### Template Not Found

**Error:** Kavenegar API error 431 (template structure mismatch)

**Solution:**
- Check template name in Kavenegar panel
- Ensure template has exactly 2 tokens: `%token` and `%token2`
- Template name must match `KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME`

---

## API Response Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | ✅ Success | SMS sent successfully |
| 401 | ❌ Error | Invalid API key |
| 431 | ❌ Error | Template structure mismatch or headers too large |
| 422 | ❌ Error | Invalid phone number |

---

## Cost

Based on testing:
- **Per SMS:** ~2,910 Rials
- **Provider:** Kavenegar shared pattern
- **Sender Number:** 10000090000 or 2000011022013

---

## Model Structure

```python
class Seller(models.Model):
    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, validators=[validate_iranian_mobile])
    phone = models.CharField(max_length=20, blank=True, null=True)
    working_fields = models.ManyToManyField(Subcategory, related_name='sellers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

## Troubleshooting

### SMS Not Received

1. Check phone number format
2. Verify API key is correct
3. Check IP is whitelisted in Kavenegar
4. Check Kavenegar balance
5. Review logs for errors

### Testing Not Working

```bash
# Check environment variables
echo $KAVENEGAR_API_KEY
echo $KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME

# Try local mode first
export SMS_NEWSLETTER_LOCAL_MODE=true
python test_sms_newsletter.py

# Then try real SMS
unset SMS_NEWSLETTER_LOCAL_MODE
export KAVENEGAR_API_KEY="your-key"
python test_sms_newsletter.py
```

### Logs

Check Django logs:

```python
# In settings.py
LOGGING = {
    'loggers': {
        'sms_newsletter': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

---

## Production Checklist

- [ ] Kavenegar account created
- [ ] API key obtained (88 chars)
- [ ] Template `SupplyerNotif` created in panel
- [ ] VPS IP (185.208.172.76) whitelisted
- [ ] Environment variables set in production `.env`
- [ ] Service code deployed
- [ ] Test SMS sent successfully
- [ ] Kavenegar balance sufficient
- [ ] Monitoring/logging enabled

---

## References

- **Kavenegar Panel:** https://panel.kavenegar.com
- **Kavenegar API Docs:** https://kavenegar.com/rest.html
- **Service File:** `sms_newsletter/services.py`
- **Model File:** `sms_newsletter/models.py`
- **Test Script:** `test_sms_newsletter.py`

---

## Support

For issues or questions:
1. Check logs: `multivendor_platform/logs/`
2. Review test summary: `SMS_NEWSLETTER_TEST_SUMMARY.md`
3. Contact Kavenegar support: https://kavenegar.com/support
4. Check Django admin for seller/template configuration

---

**Last Updated:** January 3, 2026  
**Status:** ✅ Production Ready

