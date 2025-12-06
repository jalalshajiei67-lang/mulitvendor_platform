# 🚀 Quick Start: Supplier Mini Websites

## For Suppliers (5-Minute Setup)

### 1. Login & Navigate
```
1. Go to: /login
2. Login with your supplier account
3. Click: داشبورد فروشنده (Seller Dashboard)
4. Click tab: وب‌سایت مینی (Mini Website)
```

### 2. Basic Setup (Required)
**Settings Tab:**
- [ ] Upload banner image (recommended: 1920x400px)
- [ ] Choose brand colors (primary & secondary)
- [ ] Add company slogan
- [ ] Enter year established
- [ ] Add employee count

**Click:** ذخیره تنظیمات (Save Settings)

### 3. Add Content (Recommended)
**Portfolio Tab:**
- [ ] Add 3-5 project examples
- [ ] Upload project images
- [ ] Write descriptions

**Team Tab:**
- [ ] Add key team members
- [ ] Upload their photos
- [ ] Add positions

### 4. View Your Website
**Click:** پیش‌نمایش سایت (Preview Site)  
**Share:** `/suppliers/{your-id}`

---

## For Admins (Configuration)

### Backend Setup ✅ (Already Done)
- Models created
- Migrations applied
- APIs working
- Admin configured

### What You Can Do:
```
1. Django Admin: /admin
2. Navigate to: Users > Supplier Profiles
3. Edit any supplier
4. See inline Portfolio & Team management
5. Moderate content if needed
```

---

## For Developers (Testing)

### Test Public View:
```bash
1. Visit: /suppliers
2. Click any supplier
3. Verify all tabs work:
   - Overview ✅
   - Products ✅
   - Portfolio ✅
   - Team ✅
   - Certifications ✅
   - Reviews ✅
   - Contact ✅
```

### Test Dashboard:
```bash
1. Login as supplier
2. Go to: /seller/dashboard?tab=miniwebsite
3. Test all sub-tabs:
   - Settings ✅
   - Portfolio ✅
   - Team ✅
   - Messages ✅
```

### Test Contact Form:
```bash
1. Visit supplier page as guest
2. Go to Contact tab
3. Fill and submit form
4. Login as supplier
5. Check Messages inbox
6. Verify message appears
```

---

## API Quick Reference

### Get Supplier Data:
```javascript
GET /api/users/suppliers/{id}/
```

### Add Portfolio Item:
```javascript
POST /api/users/supplier-portfolio/
Headers: { Authorization: 'Token YOUR_TOKEN' }
Body: FormData with title, description, image, etc.
```

### View Messages:
```javascript
GET /api/users/supplier-contact/
Headers: { Authorization: 'Token YOUR_TOKEN' }
```

---

## Troubleshooting

### "Components not found" error:
```bash
# Check components exist:
ls multivendor_platform/front_end/nuxt/components/supplier/

# Should see:
# MiniWebsiteSettings.vue ✅
# PortfolioManager.vue ✅
# TeamManager.vue ✅
# ContactMessagesInbox.vue ✅
```

### "Tab not showing" issue:
```bash
# Clear browser cache
# Restart Nuxt dev server
npm run dev
```

### Image upload not working:
```bash
# Check Django settings for MEDIA_ROOT
# Ensure directory has write permissions
chmod 755 media/
```

---

## Key URLs

### Public Pages:
- Supplier Directory: `/suppliers`
- Supplier Page: `/suppliers/{id}`

### Dashboard:
- Seller Dashboard: `/seller/dashboard`
- Mini Website Tab: `/seller/dashboard?tab=miniwebsite`

### API Base:
- API Root: `/api/users/`
- Portfolio: `/api/users/supplier-portfolio/`
- Team: `/api/users/supplier-team/`
- Contact: `/api/users/supplier-contact/`

---

## Feature Checklist

### Public Website Features:
- [x] Custom branding (colors, banner)
- [x] Hero section with metrics
- [x] Tabbed navigation
- [x] Portfolio gallery with lightbox
- [x] Team member profiles
- [x] Certifications & awards
- [x] Product catalog
- [x] Customer reviews
- [x] Contact form
- [x] Social media links
- [x] Video embed
- [x] SEO optimization
- [x] Mobile responsive
- [x] RTL support

### Dashboard Features:
- [x] Settings editor
- [x] Banner upload
- [x] Color picker
- [x] Portfolio manager (CRUD)
- [x] Team manager (CRUD)
- [x] Message inbox
- [x] Read/unread tracking
- [x] Preview link

---

## Success Criteria

✅ Supplier can customize their mini website  
✅ Portfolio items display correctly  
✅ Team members show with photos  
✅ Contact form sends messages  
✅ Messages appear in inbox  
✅ Brand colors apply correctly  
✅ Mobile responsive works  
✅ RTL layout correct  
✅ No console errors  
✅ SEO meta tags working  

---

## Support Resources

1. **Full Documentation**: `SUPPLIER_MINI_WEBSITES_COMPLETE.md`
2. **Implementation Details**: `SUPPLIER_MINI_WEBSITES_IMPLEMENTATION_SUMMARY.md`
3. **Components**: Check `components/supplier/` directory
4. **API Docs**: Check `users/views.py` docstrings

---

## 🎉 You're Ready!

The system is **100% complete** and ready to use. Enjoy your new Alibaba.com-style supplier mini websites!

