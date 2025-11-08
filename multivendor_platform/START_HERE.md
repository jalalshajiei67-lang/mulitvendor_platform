# Quick Start Guide - Fix Products Not Showing

## Problem
Your products are in the database but not showing on the frontend.

## Quick Solution

### Option 1: Use the Batch Files (Easiest)

1. **Double-click** `start_backend.bat` 
   - This starts the Django server
   - Keep this window open
   
2. **Double-click** `start_frontend.bat`
   - This starts the Vue frontend
   - Keep this window open

3. **Open your browser** to: http://localhost:5173/products

4. **Check if products appear**
   - If YES: Problem solved! ✅
   - If NO: Continue to Step 4

4. **Press F12** in browser and check the Console tab for errors

### Option 2: Manual Start

#### Terminal 1 - Backend:
```bash
cd multivendor_platform
..\venv\Scripts\activate
python manage.py runserver
```

#### Terminal 2 - Frontend:
```bash
cd front_end
npm run dev
```

Then open: http://localhost:5173/products

## What to Look For

### In Backend Terminal:
You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### In Frontend Terminal:
You should see:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

### In Browser Console (F12):
You should NOT see:
- ❌ CORS errors
- ❌ Network errors
- ❌ Connection refused errors

You SHOULD see:
- ✅ "ProductList mounted, fetching data..."
- ✅ "Product Store: Fetching products..."
- ✅ Products appearing on the page

## Status Check

Run this to verify your products are in the database:
```bash
cd multivendor_platform
python check_products.py
```

## Still Not Working?

If products still don't show:

1. **Copy ALL the text from the browser console** (F12 > Console tab)
2. **Take a screenshot** of the products page
3. **Run** `python check_products.py` and copy the output
4. **Report back** with all three pieces of information

## Common Problems

| Problem | Solution |
|---------|----------|
| Can't access http://localhost:5173 | Frontend not running - run `start_frontend.bat` |
| Network error in console | Backend not running - run `start_backend.bat` |
| Products show 0 | Check `check_products.py` output |
| CORS errors | Already fixed in code, clear browser cache |

## Files Created for You

- ✅ `start_backend.bat` - Starts Django server
- ✅ `start_frontend.bat` - Starts Vue frontend  
- ✅ `check_products.py` - Shows product status
- ✅ `TROUBLESHOOTING_PRODUCTS_NOT_SHOWING.md` - Detailed guide

## Need More Help?

Read the detailed guide:
- `TROUBLESHOOTING_PRODUCTS_NOT_SHOWING.md`

