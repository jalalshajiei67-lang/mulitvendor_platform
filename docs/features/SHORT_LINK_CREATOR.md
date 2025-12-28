# Short Link Creator for Marketing Campaigns

A minimal short link system integrated into Django admin for tracking marketing campaign performance.

## Features

- **Custom Short Links**: Create custom short codes (e.g., `/s/summer-sale`)
- **Click Tracking**: Track total clicks and unique visitors
- **Device Detection**: Identify mobile, tablet, or desktop users
- **IP Tracking**: Record visitor IP addresses
- **Timestamp Logging**: Track when each click occurred
- **Campaign Management**: Organize links by campaign name
- **Active/Inactive Toggle**: Enable or disable links as needed

## Usage

### Creating a Short Link

1. Go to Django Admin → Pages → Short Links
2. Click "Add Short Link"
3. Fill in:
   - **Short Code**: Custom code for the link (e.g., `summer-sale`)
   - **Target URL**: Internal page URL (e.g., `/products/special-offer`)
   - **Campaign Name**: Optional name for organization
   - **Active**: Check to enable the link

### Accessing Short Links

Short links are accessed via: `yoursite.com/s/{short_code}`

Example: `yoursite.com/s/summer-sale` → redirects to target URL

### Viewing Statistics

1. In the Short Links list, you'll see:
   - Click count
   - Unique visitor count
   
2. Click on a short link to see:
   - Detailed click history
   - IP addresses
   - Device types
   - Timestamps

### Tracking Details

Each click records:
- **IP Address**: Visitor's IP
- **Device Type**: Mobile, Tablet, Desktop, or Unknown
- **Timestamp**: Exact time of click

### Metrics

- **Click Count**: Total number of clicks
- **Unique Visitors**: Count of distinct IP addresses

## Database Tables

- `pages_shortlink`: Stores short link configurations
- `pages_shortlinkclick`: Stores individual click records

## API Endpoints

Short links work via direct URL access (no API needed):
- `GET /s/{short_code}` - Redirects to target URL and tracks click

## Admin Interface

### Short Link Admin
- List view shows: code, campaign, target, stats, status
- Inline click history when editing
- Search by code, campaign, or target URL
- Filter by active status and creation date

### Click Admin
- Read-only view of all clicks
- Filter by device type, date, and link
- Search by IP or short code
- Date hierarchy for easy navigation

## Implementation Files

- `pages/models.py` - ShortLink and ShortLinkClick models
- `pages/admin.py` - Admin interface configuration
- `pages/views.py` - Redirect handler with tracking
- `pages/migrations/0004_shortlink_shortlinkclick.py` - Database migration
- `multivendor_platform/urls.py` - URL routing

## Migration

Run migration to create tables:
```bash
python manage.py migrate pages
```

## Notes

- Short codes must be unique
- Only active links will redirect
- Inactive links return 404
- Click tracking is automatic
- No authentication required for public links
