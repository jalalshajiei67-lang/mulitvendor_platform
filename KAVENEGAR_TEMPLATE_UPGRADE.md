# Kavenegar Template Upgrade Guide

## ✅ Current Status: Working with Limited Filter

**Current Template:** `SupplyerNotif`
```
سلام، %token عزیز برای %token2 مشتری جدیدی منتظر شماست.
ایندکسو
indexo.ir/s/notif
```

**Result:**
- ✅ Full name without spaces: "رجبعلیطیبینژاد"
- ⚠️ Only first word of filter: "خط"

**SMS Example:**
```
سلام، رجبعلیطیبینژاد عزیز برای خط مشتری جدیدی منتظر شماست.
ایندکسو
indexo.ir/s/notif
```

---

## 🚀 Recommended Upgrade: Use %token10 for Better Filter Display

### Kavenegar Token Rules (from provider):

| Token | Space Limit | Example |
|-------|-------------|---------|
| `%token` | No spaces | "رجبعلیطیبپور" |
| `%token2` | No spaces | "خط" |
| `%token3` | No spaces | "نوار" |
| `%token10` | Up to 4 spaces | "خط تولید نوار بهداشتی صنعتی" |
| `%token20` | Up to 8 spaces | (even longer text) |

---

## 📝 Step 1: Create New Template in Kavenegar Panel

### Option A: Update Existing Template (Recommended)

1. Go to https://panel.kavenegar.com
2. Navigate to: **Settings → Templates**
3. Find template: **SupplyerNotif**
4. Click **Edit**
5. Update content to:

```
سلام، %token عزیز
برای %token10 مشتری جدیدی منتظر شماست.
ایندکسو
indexo.ir/s/notif
```

6. Save and wait for approval (usually instant)

### Option B: Create New Template

1. Go to https://panel.kavenegar.com
2. Navigate to: **Settings → Templates**
3. Click **Create New Template**
4. Template Name: **SupplierNotifFull**
5. Content:

```
سلام، %token عزیز
برای %token10 مشتری جدیدی منتظر شماست.
ایندکسو
indexo.ir/s/notif
```

6. Save and wait for approval

---

## 🔧 Step 2: Update Environment Variable (if using Option B)

If you created a new template, update your `.env` file:

```bash
# Old
KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME=SupplyerNotif

# New (if you created new template)
KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME=SupplierNotifFull
```

---

## ✅ Step 3: Test the New Template

Run the test script:

```bash
cd multivendor_platform/multivendor_platform
source ../../venv/bin/activate

export KAVENEGAR_API_KEY="your-api-key"
export KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME="SupplyerNotif"  # or SupplierNotifFull

python test_sms_newsletter.py
```

---

## 📊 Expected Results

### With Old Template (%token + %token2):
```
Name: رجبعلی طیب پور
Filter: خط تولید نوار بهداشتی صنعتی

SMS:
سلام، رجبعلیطیبپور عزیز برای خط مشتری جدیدی منتظر شماست.
ایندکسو
indexo.ir/s/notif
```

### With New Template (%token + %token10):
```
Name: رجبعلی طیب پور
Filter: خط تولید نوار بهداشتی صنعتی

SMS:
سلام، رجبعلیطیبپور عزیز
برای خط تولید نوار بهداشتی صنعتی مشتری جدیدی منتظر شماست.
ایندکسو
indexo.ir/s/notif
```

**Much better!** ✅ Full filter with up to 5 words (4 spaces)

---

## 🎯 Benefits of Upgrade

| Aspect | Old Template | New Template |
|--------|-------------|--------------|
| **Name** | Full (no spaces) ✅ | Full (no spaces) ✅ |
| **Filter** | First word only ⚠️ | Up to 5 words ✅ |
| **Clarity** | Limited | Much better |
| **Example** | "خط" | "خط تولید نوار بهداشتی صنعتی" |

---

## 🔍 Technical Details

### Code Changes Made

The service now automatically detects which template you're using:

```python
# Auto-detection
use_token10 = 'token10' in template_name.lower() or template_name == 'SupplierNotifFull'

if use_token10:
    # Use %token10 - supports up to 4 spaces
    params = {
        'token': name_without_spaces,
        'token10': full_filter  # Up to 5 words
    }
else:
    # Use %token2 - no spaces
    params = {
        'token': name_without_spaces,
        'token2': first_word_only
    }
```

### Filter Truncation Logic

If filter has more than 4 spaces (5+ words), it's automatically truncated:

```python
"خط تولید نوار بهداشتی صنعتی پلاستیکی" (6 words, 5 spaces)
→ "خط تولید نوار بهداشتی صنعتی" (5 words, 4 spaces) ✅
```

---

## ⚠️ Important Notes

1. **Name without spaces works:** "رجبعلی طیبی نژاد" → "رجبعلیطیبینژاد" ✅
2. **Filter with spaces works with %token10:** "خط تولید نوار..." ✅
3. **Template must be approved:** Wait for Kavenegar approval (usually instant)
4. **Backward compatible:** Code works with both old and new templates
5. **No code changes needed:** Just update template in Kavenegar panel

---

## 🚀 Deployment

Once template is approved:

1. **Option A (Recommended):** Just updated existing template → No changes needed
2. **Option B:** Created new template → Update environment variable on VPS

```bash
# On VPS
echo 'KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME=SupplierNotifFull' >> .env

# Restart services
docker-compose restart backend
```

---

## 📞 Support

If you have issues:
1. Check template is approved in Kavenegar panel
2. Verify environment variable is set correctly
3. Check logs: `multivendor_platform/logs/`
4. Contact Kavenegar support: https://kavenegar.com/support

---

**Status:** ✅ Ready to upgrade!  
**Recommendation:** Update template to use `%token10` for much better filter display

