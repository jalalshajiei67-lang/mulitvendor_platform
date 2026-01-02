# Testing SMS Newsletter Locally with Kavenegar

This guide helps you test the SMS newsletter functionality locally using the real Kavenegar API.

## Prerequisites

1. Kavenegar account with API key
2. Kavenegar template "SupplyerNotif" configured with `%token` and `%token2`
3. Local IP address whitelisted in Kavenegar panel

## Step 1: Get Your Local IP Address

Run the helper script:

```bash
./get_local_ip.sh
```

Or manually check:
```bash
# Using Python
python3 -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print(s.getsockname()[0]); s.close()"

# Or visit
# https://whatismyipaddress.com/
```

## Step 2: Add IP to Kavenegar Whitelist

1. Log in to [Kavenegar Panel](https://panel.kavenegar.com)
2. Navigate to: **Membership** → **IP Whitelist**
   - Direct link: https://panel.kavenegar.com/client/membership/ip
3. Click **Add IP** or **افزودن IP**
4. Enter your local IP address (e.g., `10.38.126.221`)
5. Save and wait 2-3 minutes for changes to take effect

⚠️ **Important**: Without IP whitelisting, Kavenegar API will reject requests from your local machine.

## Step 3: Set Environment Variables

Set your Kavenegar API key and template name:

### Fish Shell:
```fish
set -x KAVENEGAR_API_KEY "your-api-key-here"
set -x KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME "SupplyerNotif"
```

### Bash/Zsh:
```bash
export KAVENEGAR_API_KEY="your-api-key-here"
export KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME="SupplyerNotif"
```

### Or in `.env` file:
```env
KAVENEGAR_API_KEY=your-api-key-here
KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME=SupplyerNotif
```

## Step 4: Verify Template Configuration

Make sure your Kavenegar template "SupplyerNotif" is:
- ✅ Active/Approved
- ✅ Has 2 tokens: `%token` and `%token2`
- ✅ Template structure matches:
  ```
  سلام، %token عزیز برای %token2 مشتری جدیدی منتظر شماست.
  ایندکسو
  indexo.ir/s/notif
  ```

## Step 5: Run the Test Script

Navigate to Django project directory:

```bash
cd multivendor_platform/multivendor_platform
```

Run the test script:

```bash
# Interactive mode (will prompt for inputs)
python test_sms_newsletter.py

# Or with arguments
python test_sms_newsletter.py 09123456789 "علی احمدی" "الکترونیک"
```

### What the Test Script Does:

1. ✅ Checks Kavenegar configuration (API key, template name)
2. ✅ Shows your local IP address
3. ✅ Tests direct API call to Kavenegar
4. ✅ Tests the service function (`send_sms_via_kavenegar`)
5. ✅ Shows detailed error messages if something fails

## Step 6: Test via Django Admin

1. Start Django server:
   ```bash
   python manage.py runserver
   ```

2. Access Django Admin:
   - URL: http://localhost:8000/admin/
   - Navigate to: **SMS Newsletter** → **Sellers**

3. Create or select a seller

4. Use the "Send SMS to selected sellers" action

## Expected Results

### ✅ Success:
- SMS sent successfully
- Message ID returned
- No error messages

### ❌ Common Errors:

#### Error 401: Unauthorized
- **Cause**: API key incorrect or IP not whitelisted
- **Solution**: 
  - Verify API key in Kavenegar panel
  - Add your IP to whitelist
  - Wait 2-3 minutes after adding IP

#### Error 431: Template Structure Mismatch
- **Cause**: Template doesn't have `%token` and `%token2`
- **Solution**: Update template in Kavenegar panel to include both tokens

#### Connection Error
- **Cause**: Internet connection issue or Kavenegar API down
- **Solution**: Check internet connection and Kavenegar status

## Local Mode (Without API Key)

If you don't set `KAVENEGAR_API_KEY`, the system automatically uses **local mode**:
- SMS content is logged to console
- No actual SMS is sent
- Useful for development without API access

To force local mode even with API key set:
```bash
export SMS_NEWSLETTER_LOCAL_MODE=true
```

## Troubleshooting

### IP Not Working?
- Check if you're behind a VPN (use VPN IP instead)
- Check if you're on a corporate network (may need to whitelist gateway IP)
- Try using your public IP: `curl ifconfig.me`

### Template Not Found?
- Verify template name matches exactly (case-sensitive)
- Check template is approved in Kavenegar panel
- Ensure template has correct token structure

### Still Having Issues?
1. Check Kavenegar panel logs for detailed errors
2. Verify API key has SMS sending permissions
3. Check account balance in Kavenegar panel
4. Contact Kavenegar support if needed

## Quick Test Checklist

- [ ] Local IP obtained: `./get_local_ip.sh`
- [ ] IP added to Kavenegar whitelist
- [ ] `KAVENEGAR_API_KEY` environment variable set
- [ ] `KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME` set (or using default)
- [ ] Template "SupplyerNotif" configured with `%token` and `%token2`
- [ ] Test script run: `python test_sms_newsletter.py`
- [ ] SMS received successfully ✅

## Next Steps

After successful local testing:
1. Test in staging environment
2. Verify SMS delivery and formatting
3. Test with real seller data
4. Deploy to production

