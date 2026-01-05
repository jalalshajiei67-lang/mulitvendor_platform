# Fix Kavenegar Error 431 - Template Structure Mismatch

## Problem
Error 431 from Kavenegar API with message: "ساختار کد صحیح نمی باشد" (The code structure is not correct)

This error occurs when the template structure in Kavenegar panel doesn't match what the code is sending.

## Current Configuration
- **Template Name**: `SupplyerNotif`
- **Tokens Sent**: 
  - `token` = seller name (e.g., "تست1")
  - `token2` = filter name (e.g., "آب شیرین کن صنعتی")

## How to Fix

### Step 1: Check Template in Kavenegar Panel
1. Log in to [Kavenegar Panel](https://panel.kavenegar.com)
2. Go to **پیامک** → **قالب‌های پیامک** (SMS → Templates)
3. Find the template named **"SupplyerNotif"**

### Step 2: Verify Template Structure
The template should be configured with **exactly 2 tokens**:
- **Token 1** (token): Seller name
- **Token 2** (token2): Filter name

### Step 3: Template Content Example
The template content should look like this:
```
سلام، %token عزیز برای %token2 مشتری جدیدی منتظر شماست.
ایندکسو
indexo.ir/s/notif
```

**Important**: 
- Use `%token` and `%token2` (not `%token10`, `%token20`, etc.)
- The template must have exactly 2 tokens

### Step 4: Common Issues and Solutions

#### Issue 1: Template Doesn't Exist
**Solution**: Create a new template named "SupplyerNotif" with 2 tokens

#### Issue 2: Template Has Wrong Number of Tokens
**Solution**: Edit the template to use exactly 2 tokens (`%token` and `%token2`)

#### Issue 3: Template Uses Different Token Names
**Solution**: Update the template to use `%token` and `%token2` (standard Kavenegar format)

#### Issue 4: Template Name Mismatch
**Solution**: Either:
- Rename the template in Kavenegar panel to "SupplyerNotif"
- OR update `KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME` in `.env` to match your template name

### Step 5: Test After Fix
After fixing the template, test by sending an SMS from the admin panel. The error should be resolved.

## Code Changes Made
- Added better error handling for error 431
- Added detailed error messages in Persian
- Added logging with token values for debugging

## Environment Variable
Make sure this is set in your `.env` file:
```bash
KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME=SupplyerNotif
```

## Verification
After fixing, you should see:
- Status code: 200 (success)
- SMS sent successfully
- No error 431

## Need Help?
If the issue persists:
1. Check Kavenegar panel logs for detailed error messages
2. Verify API key is correct
3. Contact Kavenegar support if template structure is correct but still getting errors


