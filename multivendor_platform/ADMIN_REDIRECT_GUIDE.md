# Admin Auto-Redirect to Django Admin Panel

## Overview
Admins and superusers are now automatically redirected to the Django Admin Panel when they log in, instead of going to the custom Vue.js admin dashboard.

## How It Works

When a user with `is_staff=True` (admin/superuser) logs in through the frontend:
1. Authentication happens via the API
2. The frontend detects the user is an admin (`is_staff: true`)
3. User is automatically redirected to Django Admin Panel at `/admin/`

## Files Modified

### 1. **LoginView.vue**
- Updated login handler to redirect admins to Django admin panel
- Non-admin users are redirected to their respective dashboards (buyer/seller)

### 2. **App.vue**
- Changed navigation menu item for admins
- "Admin Dashboard" → "Django Admin Panel"
- Clicking the menu item opens Django admin

### 3. **router/index.js**
- Updated navigation guard
- Admins accessing guest-only pages (like `/login`) are redirected to Django admin

### 4. **config.js** (NEW)
- Created centralized configuration file
- Django admin URL is configurable
- Default: `http://127.0.0.1:8000/admin/`

## Configuration

### Development (Default)
The system is pre-configured for local development:
```javascript
djangoAdminUrl: 'http://127.0.0.1:8000/admin/'
```

### Production Setup
To change the Django admin URL for production:

**Option 1: Environment Variable (Recommended)**
1. Create a `.env` file in `front_end/` directory:
```env
VITE_DJANGO_ADMIN_URL=https://yourdomain.com/admin/
```

**Option 2: Edit config.js directly**
```javascript
// src/config.js
export const config = {
  djangoAdminUrl: 'https://yourdomain.com/admin/',
}
```

## User Flow Examples

### Admin User Login:
1. Admin visits `http://localhost:5173/login`
2. Enters credentials (username/password)
3. Clicks "Login"
4. ✅ **Automatically redirected to Django Admin Panel** (`http://127.0.0.1:8000/admin/`)

### Seller User Login:
1. Seller visits `http://localhost:5173/login`
2. Enters credentials
3. Clicks "Login"
4. ✅ **Redirected to Seller Dashboard** (`/seller/dashboard`)

### Buyer User Login:
1. Buyer visits `http://localhost:5173/login`
2. Enters credentials
3. Clicks "Login"
4. ✅ **Redirected to Buyer Dashboard** (`/buyer/dashboard`)

## Navigation Menu

### For Admins (when logged in):
- Menu shows: **"Django Admin Panel"** with shield icon
- Clicking it opens Django admin in same tab
- Also shows Seller/Buyer dashboards if role is "both"

### For Sellers:
- Menu shows: **"Seller Dashboard"** with store icon

### For Buyers:
- Menu shows: **"Buyer Dashboard"** with dashboard icon

## Django Admin Panel Features

When admins access the Django admin panel, they have access to:

✅ **User Management:**
- View, edit, create, delete users
- Manage UserProfiles (roles, verification, blocking)
- Manage BuyerProfiles
- Manage VendorProfiles (approve sellers)

✅ **Product Management:**
- View all products
- Edit product details
- Approve/reject products

✅ **Order Management:**
- View all orders
- Update order status
- Manage payments

✅ **Advertisement Management:**
- View all seller ads
- Approve/reject ads
- Manage ad images

✅ **Review Management:**
- View all product reviews
- Approve/disapprove reviews
- Manage review content

✅ **Activity Logs:**
- Track all user activities
- Monitor system usage
- View login/logout records

✅ **Blog Management:**
- Create/edit blog posts
- Manage blog categories
- Moderate comments

✅ **System Configuration:**
- Departments, Categories, Subcategories
- Site settings
- Permission management

## Creating Admin Users

### Method 1: Command Line (Superuser)
```bash
python manage.py createsuperuser
```
This creates a superuser with full admin access.

### Method 2: Django Admin (Regular Staff)
1. Login to Django admin as superuser
2. Go to Users
3. Click "Add User"
4. Set username and password
5. Check "Staff status" checkbox
6. Save

### Method 3: Register then Promote
1. User registers through frontend
2. Admin logs into Django admin
3. Finds user in Users list
4. Edits user → Check "Staff status"
5. Save

## Security Notes

1. **Session Authentication**: Django admin uses session authentication, separate from the API token authentication
2. **First Login**: Admin must log in through Django admin first time after redirect
3. **Auto-login**: Frontend doesn't automatically log admin into Django admin (security)
4. **CORS**: Django admin and Vue frontend are separate applications

## Troubleshooting

### Admin redirect not working?
- Check if user has `is_staff=True` in Django admin
- Verify Django server is running on correct port
- Check browser console for errors

### Can't access Django admin?
- Ensure Django server is running: `python manage.py runserver`
- Verify URL is correct: `http://127.0.0.1:8000/admin/`
- Make sure user is staff/superuser

### Want to use custom admin dashboard instead?
If you want to keep the custom Vue.js admin dashboard, revert these changes:
1. In `LoginView.vue`: Change `window.location.href = config.djangoAdminUrl` back to `router.push('/admin/dashboard')`
2. In `App.vue`: Change click handler back to `$router.push('/admin/dashboard')`
3. In `router/index.js`: Change redirect back to `next('/admin/dashboard')`

## Benefits of Django Admin Redirect

✅ **Full-featured**: Django admin has all management tools built-in
✅ **Secure**: Uses Django's robust authentication and permissions
✅ **Efficient**: No need to duplicate admin features in frontend
✅ **Mature**: Proven, well-tested admin interface
✅ **Extensible**: Easy to customize with Django admin customization
✅ **Separate concerns**: Admin operations separated from user-facing app

---

**Your admin users will now have a streamlined experience with automatic access to the powerful Django admin panel!**

