# Manual Redirect Management Tool

## Overview

A Django admin tool for managing URL redirects. This allows administrators to create, edit, and manage redirects directly from the Django admin dashboard.

## Features

✅ **Admin Interface**: Full CRUD operations for redirects  
✅ **301/302 Redirects**: Support for both permanent and temporary redirects  
✅ **Active/Inactive Toggle**: Enable or disable redirects without deleting them  
✅ **Notes Field**: Add notes about why redirects were created  
✅ **Automatic Tracking**: Tracks who created each redirect and when  
✅ **Bulk Actions**: Activate/deactivate multiple redirects at once  
✅ **Search & Filter**: Search by path, filter by status and type  

## Setup

### 1. Create Migration

After deploying the code, create the database migration:

```bash
python manage.py makemigrations pages
python manage.py migrate
```

### 2. Access in Admin

1. Go to Django Admin: `https://your-domain.com/admin/`
2. Navigate to **Pages** → **Redirects**
3. Click **Add Redirect** to create a new redirect

## Usage

### Creating a Redirect

1. **From Path**: Enter the old URL path (must start with `/`)
   - Example: `/old-page` or `/products/123`

2. **To Path**: Enter the new URL (can be relative or absolute)
   - Relative: `/new-page` (will use current domain)
   - Absolute: `https://example.com/new-page`

3. **Redirect Type**:
   - **301 Permanent**: Use for permanent moves (better for SEO)
   - **302 Temporary**: Use for temporary redirects

4. **Active**: Check to enable the redirect

5. **Notes**: Optional notes about the redirect

### Example Redirects

#### Backend to Frontend Redirect
- **From**: `/products/8`
- **To**: `https://indexo.ir/products/8`
- **Type**: 301 Permanent
- **Purpose**: Redirect backend URLs to frontend

#### Old URL to New URL
- **From**: `/old-product-page`
- **To**: `/products/new-product-page`
- **Type**: 301 Permanent
- **Purpose**: URL structure change

#### External Redirect
- **From**: `/external-link`
- **To**: `https://external-site.com/page`
- **Type**: 302 Temporary
- **Purpose**: Temporary external link

## How It Works

1. **Middleware**: The `RedirectMiddleware` checks every request for matching redirects
2. **Early Processing**: Redirects are checked before other routes
3. **Excluded Paths**: Admin, API, static files are excluded from redirect checking
4. **Query Parameters**: Query strings are preserved in redirects

## Admin Features

### List View
- Shows all redirects with status indicators (✓/✗)
- Displays: From Path → To Path, Type, Status, Dates
- Searchable by path and notes
- Filterable by status, type, and date

### Bulk Actions
- **Activate Redirects**: Enable multiple redirects at once
- **Deactivate Redirects**: Disable multiple redirects at once

### Form Fields
- **From Path**: Source URL (required, must start with `/`)
- **To Path**: Destination URL (required)
- **Redirect Type**: 301 or 302 (default: 301)
- **Active**: Enable/disable toggle
- **Notes**: Optional admin notes
- **Created By**: Auto-filled with current user
- **Created At**: Auto-filled timestamp
- **Updated At**: Auto-updated timestamp

## Technical Details

### Model: `pages.Redirect`

**Fields:**
- `from_path`: CharField (500 chars, unique, indexed)
- `to_path`: CharField (500 chars)
- `redirect_type`: CharField (choices: 301, 302)
- `is_active`: BooleanField
- `notes`: TextField (optional)
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)
- `created_by`: ForeignKey to User

**Indexes:**
- `from_path` (unique)
- `from_path + is_active` (composite)

### Middleware: `pages.middleware.RedirectMiddleware`

**Excluded Paths:**
- `/admin/`
- `/api/`
- `/static/`
- `/media/`
- `/robots.txt`
- `/sitemap.xml`
- `/health/`
- `/tinymce/`
- `/favicon.ico`

**Processing:**
1. Checks if path is excluded
2. Queries active redirects matching the path
3. Builds absolute URL if needed
4. Preserves query parameters
5. Returns redirect response (301 or 302)

## Best Practices

1. **Use 301 for Permanent Moves**: Better for SEO, tells search engines the move is permanent
2. **Use 302 for Temporary**: Use when content might move back
3. **Test Before Activating**: Create redirect with `is_active=False`, test, then activate
4. **Add Notes**: Document why redirects were created
5. **Monitor**: Check redirects periodically to ensure they're still needed
6. **Clean Up**: Remove old redirects that are no longer needed

## Troubleshooting

### Redirect Not Working

1. **Check if Active**: Ensure `is_active=True`
2. **Check Path Match**: From path must match exactly (including trailing slash)
3. **Check Excluded Paths**: Some paths are excluded from redirect checking
4. **Check Middleware Order**: RedirectMiddleware must be early in middleware stack

### Database Errors

If you see database errors:
```bash
python manage.py makemigrations pages
python manage.py migrate
```

### Performance

- Redirects are cached in memory (Django's default caching)
- Database queries are optimized with indexes
- Only active redirects are queried

## Integration with Existing Redirects

This tool works alongside:
- ✅ Automatic backend-to-frontend redirects (products, categories, etc.)
- ✅ robots.txt blocking
- ✅ X-Robots-Tag headers

Manual redirects take precedence over automatic redirects.

## Examples

### Redirect Backend Product URLs

```
From: /products/8
To: https://indexo.ir/products/8
Type: 301
Active: ✓
Notes: Redirect backend URL to frontend for SEO
```

### Redirect Old Category Structure

```
From: /old-category-name
To: /categories/new-category-name
Type: 301
Active: ✓
Notes: Category URL structure changed
```

### Temporary Maintenance Redirect

```
From: /maintenance-page
To: /maintenance
Type: 302
Active: ✓
Notes: Temporary redirect during maintenance
```

