# Products Not Showing on Frontend - Troubleshooting Guide

## Problem
Products are visible in Django Admin but not showing on the frontend.

## Root Cause Analysis

Based on my investigation:
- ✅ **Products exist in database**: 3 products found
- ✅ **Products are active**: All show `is_active: True`
- ✅ **Django API is working**: Returns products correctly at http://127.0.0.1:8000/api/products/
- ✅ **CORS is configured**: Django allows frontend requests
- ⚠️ **Frontend connection**: Need to verify frontend is running and connecting to backend

## Products in Database

```
ID: 5 - جت پرینتر دستی EBS مدل E250 #7460
  ✅ is_active: True
  ✅ primary_category: ماشین آلات بسته بندی
  
ID: 4 - لیزر CO2 ویدئوجت مدل 3130 #9930
  ✅ is_active: True
  ✅ primary_category: ماشین آلات بسته بندی
  
ID: 2 - جت پرینتر صنعتی دومینو A320 #9396
  ✅ is_active: True
  ⚠️ primary_category: None (might be hidden)
```

## Solution Steps

### Step 1: Ensure Both Servers Are Running

#### Start Django Backend (Terminal 1):
```bash
cd multivendor_platform\multivendor_platform
..\venv\Scripts\activate
python manage.py runserver
```

The backend should be running at: http://127.0.0.1:8000

#### Start Vue Frontend (Terminal 2):
```bash
cd multivendor_platform\front_end
npm run dev
```

The frontend should be running at: http://localhost:5173

### Step 2: Verify API is Accessible

Open browser and go to:
- http://127.0.0.1:8000/api/products/

You should see JSON data with 3 products.

### Step 3: Clear Browser Cache

1. Open the frontend: http://localhost:5173
2. Press `F12` to open Developer Tools
3. Go to "Console" tab to check for errors
4. Go to "Network" tab
5. Check if requests to http://127.0.0.1:8000/api/products/ are being made
6. If there are CORS errors, the backend configuration needs adjustment

### Step 4: Check Browser Console

When you open the products page, you should see logs like:
```
ProductList mounted, fetching data...
Product Store: Fetching products with params: ...
API: getProducts called with params: ...
```

If you see errors instead, that will tell us what's wrong.

### Step 5: Test API Directly

Open your browser to:
http://localhost:5173/products

The products should appear. If not, check the browser console for errors.

## Common Issues and Fixes

### Issue 1: Frontend Not Running
**Symptom**: Can't access http://localhost:5173
**Fix**: Run `npm run dev` in the front_end directory

### Issue 2: Backend Not Running
**Symptom**: Network errors in console, 'ERR_CONNECTION_REFUSED'
**Fix**: Run `python manage.py runserver` in the Django directory

### Issue 3: CORS Errors
**Symptom**: Browser console shows CORS policy errors
**Fix**: Already configured in settings.py (CORS_ALLOW_ALL_ORIGINS = True)

### Issue 4: Products Have No primary_category
**Symptom**: Some products don't appear
**Fix**: In Django Admin, edit each product and set the "Primary Category" field

## Quick Fix Script

I've created a script to check products status. Run it from the Django directory:

```bash
cd multivendor_platform\multivendor_platform
..\venv\Scripts\activate
python check_products.py
```

This will show you all products and their status.

## Need to Set Primary Category?

If products are missing primary_category, run this in Django shell:

```bash
cd multivendor_platform\multivendor_platform
..\venv\Scripts\activate
python manage.py shell
```

Then:
```python
from products.models import Product, Category

# Get a product without primary_category
product = Product.objects.get(id=2)

# Set primary_category (example - use the actual category ID)
category = Category.objects.get(name="ماشین آلات بسته بندی")
product.primary_category = category
product.save()
```

## Next Steps

1. ✅ Start both servers (Django + Vue)
2. ✅ Open http://localhost:5173/products
3. ✅ Open browser console (F12) and check for errors
4. ✅ If you see errors, report them to me

## Contact

If products still don't show after following these steps, please provide:
1. Screenshot of browser console errors
2. Output of `python check_products.py`
3. Screenshot of Django Admin showing the product

