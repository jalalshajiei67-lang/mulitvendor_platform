# 🔧 Fix Media Files 404 Errors - Complete Guide

## 📋 Problem Summary

Category and subcategory images are returning 404 errors:
- `pharmecutical_machineries.webp` - 404
- `cosmetic_machinery_6LaXvMg.webp` - 404

**Root Cause**: The database has image file references, but the actual image files don't exist on the production server.

---

## ✅ Solution: Upload Images via Production Admin Panel

### Step 1: Access Production Admin Panel

1. Open your browser and go to: `https://multivendor-backend.indexo.ir/admin/`
2. Login with your superuser credentials
3. Navigate to **Products** → **Categories** (or **Departments** / **Subcategories**)

### Step 2: Identify Items with Missing Images

Look for categories/departments/subcategories that show:
- Broken image icons
- Empty image fields
- Or check the browser console for 404 errors on specific images

### Step 3: Upload Images

For each item with missing images:

1. Click on the item name to edit it
2. Scroll to the **Image** field
3. Click **Choose File** and select the appropriate image
4. **Important**: Use WebP format for best performance (`.webp` files)
   - Or use PNG/JPG and Django will handle them
5. Fill in the **Image Alt Text** field for SEO
6. Click **Save**

### Step 4: Verify Images Are Accessible

After uploading, verify the image URL works:
1. Right-click on the image in the admin panel
2. Choose "Open image in new tab"
3. Verify it loads correctly at: `https://multivendor-backend.indexo.ir/media/category_images/...`

---

## 🎨 Image Guidelines

### Recommended Image Specifications

#### Departments
- **Size**: 400x400px minimum
- **Format**: WebP (preferred), PNG, or JPG
- **Aspect Ratio**: 1:1 (square)
- **Max File Size**: 500KB

#### Categories
- **Size**: 300x300px minimum
- **Format**: WebP (preferred), PNG, or JPG
- **Aspect Ratio**: 1:1 (square)
- **Max File Size**: 300KB

#### Subcategories
- **Size**: 200x200px minimum
- **Format**: WebP (preferred), PNG, or JPG
- **Aspect Ratio**: 1:1 (square)
- **Max File Size**: 200KB

### Converting Images to WebP

If you have PNG/JPG images and want to convert them to WebP for better performance:

**Using Online Tools:**
- https://cloudconvert.com/webp-converter
- https://www.freeconvert.com/webp-converter

**Using Command Line (ImageMagick):**
```bash
# Convert single image
convert input.jpg -quality 80 output.webp

# Convert all JPG images in a directory
for img in *.jpg; do convert "$img" -quality 80 "${img%.jpg}.webp"; done
```

---

## 🚀 Alternative: Bulk Upload Media Files

If you have many images to upload, you can use Django shell on production:

### Method 1: Using CapRover CLI

1. Login to CapRover:
   ```bash
   caprover login
   ```

2. SSH into the backend container:
   ```bash
   caprover exec --appName multivendor-backend
   ```

3. Enter Django shell:
   ```bash
   python manage.py shell
   ```

4. Upload images programmatically:
   ```python
   from products.models import Category
   from django.core.files import File
   
   # Example: Update a specific category
   cat = Category.objects.get(slug='pharmaceutic

al-machinery')
   with open('/path/to/image.webp', 'rb') as f:
       cat.image.save('pharmaceutical_machinery.webp', File(f), save=True)
   ```

### Method 2: Transfer Local Media Files to Production

⚠️ **Only do this if you have the correct images locally**

1. Create a tarball of your local media files:
   ```bash
   cd multivendor_platform/multivendor_platform
   tar -czf media_files.tar.gz media/
   ```

2. Upload to your VPS:
   ```bash
   scp media_files.tar.gz root@185.208.172.76:/tmp/
   ```

3. SSH into VPS:
   ```bash
   ssh root@185.208.172.76
   ```

4. Find the CapRover persistent volume path:
   ```bash
   docker volume inspect captain--multivendor-backend-media
   ```

5. Extract files to the volume:
   ```bash
   # Get the Mountpoint from the previous command
   cd /var/lib/docker/volumes/captain--multivendor-backend-media/_data/
   tar -xzf /tmp/media_files.tar.gz --strip-components=1
   chown -R 999:999 *
   ```

---

## 🔍 Troubleshooting

### Issue: Images Still Return 404 After Upload

**Check 1: Verify file exists**
```bash
# SSH into CapRover backend container
caprover exec --appName multivendor-backend

# List media files
ls -la /app/media/category_images/
```

**Check 2: Verify file permissions**
```bash
# Files should be readable (644 or 755)
chmod -R 755 /app/media/
```

**Check 3: Verify MEDIA_ROOT settings**
```bash
# In Django shell
python manage.py shell
>>> from django.conf import settings
>>> print(settings.MEDIA_ROOT)
>>> print(settings.MEDIA_URL)
```

### Issue: Can't Upload Large Images

**Solution**: Increase upload size limits

1. In CapRover dashboard → multivendor-backend → App Configs
2. Add environment variable:
   ```
   MAX_UPLOAD_SIZE=10485760  # 10MB in bytes
   ```

3. Update Django settings:
   ```python
   # settings.py
   DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
   FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
   ```

### Issue: CORS Errors When Loading Images

**Solution**: The frontend at `https://indexo.ir` should be able to load images from `https://multivendor-backend.indexo.ir` without CORS issues since we're using `<img>` tags (not AJAX).

If you still see CORS errors, check:
1. Both domains use HTTPS ✓
2. Backend CORS settings allow the frontend domain

---

## 📝 Quick Checklist

- [ ] Access production admin panel
- [ ] Go to Products → Categories (and Departments, Subcategories)
- [ ] For each item with missing image:
  - [ ] Upload appropriate image
  - [ ] Add alt text
  - [ ] Save
- [ ] Verify images load on frontend
- [ ] Check browser console for any remaining 404 errors

---

## 🎯 Expected Result

After uploading images:
- ✅ `https://multivendor-backend.indexo.ir/media/category_images/pharmaceutical_machinery.webp` - 200 OK
- ✅ Images display correctly on `https://indexo.ir/departments/machinery`
- ✅ No 404 errors in browser console

---

## 💡 Best Practice for Future

1. **Always upload images via Django admin** - This ensures they go to the correct persistent volume
2. **Use WebP format** - Better compression, faster loading
3. **Optimize images before upload** - Resize to appropriate dimensions
4. **Add alt text** - Important for SEO and accessibility
5. **Test in production** - Verify images load correctly after upload

---

**Need Help?**
- Check CapRover logs: `caprover logs --appName multivendor-backend`
- Check Django admin logs for upload errors
- Verify persistent volume is mounted correctly

