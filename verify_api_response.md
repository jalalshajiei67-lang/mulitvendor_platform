# 🔍 Verify API Response - Debugging Guide

## Step 1: Check What the API Returns

Open your browser console on `https://indexo.ir/departments/machinery` and run:

```javascript
// Check what the API returns for categories
fetch('https://multivendor-backend.indexo.ir/api/categories/?department=1')
  .then(r => r.json())
  .then(data => {
    console.log('Categories API Response:', data);
    data.results?.forEach(cat => {
      console.log(`Category: ${cat.name}`);
      console.log(`Image field: ${cat.image}`);
      console.log(`Image type: ${typeof cat.image}`);
    });
  });
```

**Expected Output:**
- If `image` is `null` or empty → Category has no image assigned
- If `image` is `/media/category_images/filename.webp` → File reference exists but file is missing
- If `image` is `https://...` → Absolute URL (shouldn't happen with current setup)

## Step 2: Verify File Exists on Server

**Option A: Via CapRover Dashboard**
1. Go to CapRover dashboard → `multivendor-backend` app
2. Open terminal/console
3. Run: `ls -la /app/media/category_images/`

**Option B: Via CapRover CLI**
```bash
caprover exec --appName multivendor-backend
ls -la /app/media/category_images/
```

**Expected:**
- If files exist: You'll see `.webp` files listed
- If directory is empty: Only `.` and `..` entries

## Step 3: Verify URL Construction

In browser console on production site:
```javascript
// Simulate what formatImageUrl does
const imagePath = '/media/category_images/pharmecutical_machineries.webp';
const backendUrl = 'https://multivendor-backend.indexo.ir';
const fullUrl = backendUrl + imagePath;
console.log('Constructed URL:', fullUrl);

// Try to fetch it
fetch(fullUrl)
  .then(r => {
    console.log('Status:', r.status);
    if (r.status === 404) {
      console.log('❌ File does not exist on server');
    } else if (r.status === 200) {
      console.log('✅ File exists');
    }
  });
```

## Step 4: Check Database Records

**Via Django Admin:**
1. Go to `https://multivendor-backend.indexo.ir/admin/products/category/`
2. Click on a category that's showing 404
3. Check the "Image" field:
   - If it shows a filename → File reference exists in DB
   - If it's empty → No image assigned

**What to Look For:**
- Database has: `category_images/pharmecutical_machineries.webp`
- File system has: File missing ❌
- Result: 404 error ✅ (confirms diagnosis)

## ✅ Confirmation Checklist

- [ ] API returns image path: `/media/category_images/...`
- [ ] Frontend constructs URL: `https://multivendor-backend.indexo.ir/media/category_images/...`
- [ ] Server returns 404: File doesn't exist
- [ ] Database has reference: Image field is not null
- [ ] File system is empty: `/app/media/category_images/` has no files

## 🎯 Conclusion

If all above checks confirm:
- ✅ API returns correct path
- ✅ Frontend constructs correct URL  
- ✅ Server returns 404
- ✅ Database has reference
- ✅ File system is empty

**Then:** Diagnosis is correct - files need to be uploaded via admin panel.

