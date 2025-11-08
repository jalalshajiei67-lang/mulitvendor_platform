# 📚 Database Migration History

**Complete history of database migrations and schema changes**

---

## 📊 Overview

This document tracks all database migrations across the project, providing context for schema evolution and helping troubleshoot migration-related issues.

---

## 🗃️ Products App Migrations

### Initial Setup

#### `0001_initial.py`
**Purpose**: Initial database schema creation  
**Created**: Initial project setup  
**Changes**:
- Created base Product model
- Created Category model
- Basic fields for product management

#### `0002_alter_category_options_category_description_and_more.py`
**Purpose**: Enhanced category features  
**Changes**:
- Added description to Category
- Updated Category model options
- Added ordering and verbose names

#### `0003_auto_20251015_1101.py`
**Purpose**: Auto-generated adjustments  
**Date**: October 15, 2025 11:01  
**Changes**:
- Auto-adjustments for field types
- Index optimizations

### Category Structure Restructure

#### `0004_alter_product_category.py`
**Purpose**: Prepare for hierarchical categories  
**Changes**:
- Altered Product-Category relationship
- Preparation for Department/Subcategory structure

#### `0005_create_department_subcategory.py`
**Purpose**: Introduce hierarchical category system  
**Changes**:
- ✅ Created Department model (top level)
- ✅ Created Subcategory model (leaf level)
- Department → Category → Subcategory hierarchy

#### `0006_add_relationships_only.py`
**Purpose**: Establish relationships between hierarchical models  
**Changes**:
- Added Department-to-Category relationships
- Added Category-to-Subcategory relationships
- Added Product-to-Subcategory relationships

#### `0007_add_remaining_fields.py`
**Purpose**: Complete hierarchical structure  
**Changes**:
- Added additional fields to Department
- Added additional fields to Subcategory
- SEO fields preparation

#### `0008_migrate_existing_data.py`
**Purpose**: Data migration for existing products  
**Changes**:
- Migrated existing products to new structure
- Preserved product-category relationships
- Data integrity checks

#### `0009_finalize_structure.py`
**Purpose**: Finalize hierarchical category structure  
**Changes**:
- Removed old relationship fields
- Enforced new structure constraints
- Cleanup of deprecated fields

### Image Management

#### `0010_add_product_image_model.py`
**Purpose**: Introduce multi-image support  
**Date**: After restructure  
**Changes**:
- ✅ Created ProductImage model
- ✅ Support for multiple images per product
- ✅ Image ordering capability
- Related name: `images`

#### `0011_migrate_existing_images.py`
**Purpose**: Migrate single image to multi-image system  
**Changes**:
- Migrated existing product.image to ProductImage
- Preserved image data
- Set is_primary flag on migrated images

#### `0012_fix_unique_constraint.py`
**Purpose**: Fix unique constraint issues  
**Changes**:
- Adjusted unique constraints on ProductImage
- Fixed ordering conflicts

#### `0013_remove_all_constraints.py`
**Purpose**: Remove problematic constraints  
**Changes**:
- Removed overly restrictive constraints
- Allowed more flexibility in data model

### SEO & Metadata Enhancements

#### `0014_add_seo_fields.py`
**Purpose**: Add SEO fields to products  
**Changes**:
- ✅ Added meta_title (60 chars)
- ✅ Added meta_description (160 chars)
- ✅ Added meta_keywords (255 chars)
- Improved search engine visibility

#### `0015_add_product_comment.py`
**Purpose**: Add product review/comment system  
**Changes**:
- ✅ Created ProductComment model
- Rating field (1-5)
- Comment text
- User relationship
- Timestamps

#### `0016_add_seo_fields_to_all_categories.py`
**Purpose**: Extend SEO to all category levels  
**Changes**:
- Added SEO fields to Department
- Added SEO fields to Category
- Added SEO fields to Subcategory
- Consistent SEO across hierarchy

#### `0016_5_populate_timestamps.py` 🔶
**Purpose**: Populate missing timestamps  
**Date**: Custom migration  
**Changes**:
- Added created_at/updated_at to existing records
- Data backfill for timestamp fields
- Ensures all records have proper timestamps

#### `0016_6_fix_null_slugs.py` 🔶
**Purpose**: Fix null slug values  
**Date**: Custom migration  
**Changes**:
- Generated slugs for records with null slugs
- Ensured slug uniqueness
- Data integrity fix

#### `0017_alter_product_options_product_canonical_url_and_more.py` ✨
**Purpose**: Advanced SEO features  
**Date**: October 16, 2025 08:24  
**Dependencies**: 0016_6_fix_null_slugs  
**Changes**:
- ✅ **Product.canonical_url** - URLField(max_length=500, blank=True, null=True)
  - For SEO canonical URLs
- ✅ **Product.image_alt_text** - CharField(max_length=125, blank=True, null=True)
  - Alt text for main image (SEO + accessibility)
- ✅ **Product.schema_markup** - TextField(blank=True, null=True)
  - JSON-LD Schema for rich snippets
- ✅ **ProductImage.alt_text** - CharField(max_length=125, blank=True, null=True)
  - Alt text for additional images
- ✅ **Product ordering** - Changed to ['-created_at']
  - Newest products first
- ✅ **Slug fields** - Updated max_length and blank=True
  - Category slug: max_length=120
  - Product slug: max_length=220
- ✅ **Timestamp fields** - Added auto_now_add, auto_now
  - Proper automatic timestamp management

### Many-to-Many Relationships

#### `0018_product_primary_category.py`
**Purpose**: Add primary category concept  
**Changes**:
- Added primary_category field to Product
- Allows featured categorization
- Better product organization

#### `0019_remove_subcategory_departments.py`
**Purpose**: Simplify category relationships  
**Changes**:
- Removed direct Department-Subcategory link
- Enforced Department → Category → Subcategory flow
- Cleaner hierarchy

#### `0020_remove_product_subcategory_product_subcategories_and_more.py`
**Purpose**: Enable multiple subcategories per product  
**Changes**:
- Changed from single subcategory to multiple
- Product can belong to multiple subcategories
- More flexible categorization

### Scraper System

#### `0021_productscrapejob.py`
**Purpose**: Add product scraping infrastructure  
**Changes**:
- ✅ Created ProductScrapeJob model
- Track scraping operations
- URL to scrape
- Status tracking (pending, running, completed, failed)
- Result storage
- Error tracking

#### `0022_add_robust_error_handling.py`
**Purpose**: Enhanced error handling for scraper  
**Changes**:
- Added error_details field
- Enhanced status tracking
- Better failure diagnosis
- Retry capability tracking

#### `0023_add_batch_reporting.py`
**Purpose**: Batch scraping reports  
**Changes**:
- Added batch tracking
- Success/failure counts
- Reporting fields
- Statistics collection

---

## 👥 Users App Migrations

### Initial Setup

#### `0001_initial.py`
**Purpose**: User system foundation  
**Changes**:
- Extended Django User model
- Created base user profiles
- Authentication setup

### Vendor/Seller System

#### `0002_sellerad_vendorprofile_contact_email_and_more.py`
**Purpose**: Vendor profile enhancements  
**Changes**:
- ✅ Created SellerAd model
- ✅ Created VendorProfile model
- Added contact_email to vendors
- Seller advertising capability

#### `0003_vendorprofile_about_vendorprofile_address_and_more.py`
**Purpose**: Detailed vendor profiles  
**Changes**:
- Added 'about' text field
- Added address field
- Added phone number
- Added business details

#### `0004_alter_buyerprofile_options_alter_sellerad_options_and_more.py`
**Purpose**: Model options and metadata  
**Changes**:
- Updated BuyerProfile options
- Updated SellerAd options
- Added verbose names
- Improved admin interface

### Supplier System

#### `0005_supplier.py`
**Purpose**: Introduce supplier management  
**Changes**:
- ✅ Created Supplier model
- Separate from vendors
- Supply chain management
- Wholesale relationships

---

## 📝 Blog App Migrations

### Initial Setup

#### `0001_initial.py`
**Purpose**: Blog system foundation  
**Changes**:
- ✅ Created BlogPost model
- ✅ Created BlogCategory model
- ✅ Created BlogComment model
- Rich text support (TinyMCE)
- Author relationships
- Category relationships

### SEO Enhancement

#### `0002_add_seo_fields.py`
**Purpose**: Add SEO to blog  
**Changes**:
- Added meta_title to BlogPost
- Added meta_description to BlogPost
- Added meta_keywords to BlogPost
- Added canonical_url to BlogPost
- Featured post capability
- Improved discoverability

---

## 📦 Orders App Migrations

### Initial Setup

#### `0001_initial.py`
**Purpose**: Order management system  
**Changes**:
- ✅ Created Order model
- ✅ Created OrderItem model
- Order status tracking
- Payment tracking
- Buyer-Seller relationships

---

## 🔍 Migration Dependencies

```
Products App:
0001 (initial)
  ↓
0002 (category enhancements)
  ↓
0003 (auto adjustments)
  ↓
0004 (category prep)
  ↓
0005 (department/subcategory) → 0006 (relationships) → 0007 (remaining fields)
  ↓
0008 (data migration) → 0009 (finalize)
  ↓
0010 (product images) → 0011 (migrate images) → 0012 (fix constraints) → 0013 (remove constraints)
  ↓
0014 (seo fields) → 0015 (comments) → 0016 (category seo)
  ↓
0016_5 (timestamps) → 0016_6 (fix slugs)
  ↓
0017 (canonical urls & schema)
  ↓
0018 (primary category) → 0019 (remove subcategory link) → 0020 (multi-subcategories)
  ↓
0021 (scraper job) → 0022 (error handling) → 0023 (batch reporting)
```

---

## ⚠️ Migration Notes & Warnings

### Custom Migrations (Requires Attention)

#### `0016_5_populate_timestamps.py`
- **Type**: Data migration
- **Risk**: Low
- **Note**: Backfills timestamps for existing records
- **Action**: Review if adding to new database

#### `0016_6_fix_null_slugs.py`
- **Type**: Data migration
- **Risk**: Low
- **Note**: Generates slugs for null values
- **Action**: Ensure slug generation logic is correct

### Migration Best Practices

✅ **Always backup before migrating**
```bash
./backup-database.sh
# OR
docker-compose exec db pg_dump -U postgres multivendor_db > backup.sql
```

✅ **Test migrations locally first**
```bash
# Create test database
docker-compose -f docker-compose.local.yml up -d
docker-compose -f docker-compose.local.yml exec backend python manage.py migrate
```

✅ **Check migration status**
```bash
python manage.py showmigrations
python manage.py migrate --plan
```

✅ **Roll back if needed**
```bash
python manage.py migrate products 0016_add_seo_fields_to_all_categories
```

---

## 🔄 Migration Workflow

### Creating New Migrations

```bash
# 1. Make model changes in models.py
# 2. Create migration
python manage.py makemigrations

# 3. Review migration file
cat products/migrations/0024_*.py

# 4. Test migration
python manage.py migrate --plan

# 5. Apply migration
python manage.py migrate

# 6. Verify
python manage.py showmigrations
```

### Squashing Migrations (Future)

When migrations get too numerous:
```bash
python manage.py squashmigrations products 0001 0023
```

---

## 📊 Current Schema Statistics

### Products App
- **Migrations**: 23 total
- **Models**: 7 (Product, ProductImage, Department, Category, Subcategory, ProductComment, ProductScrapeJob)
- **Fields**: ~80+ across all models
- **Relationships**: Many-to-One, Many-to-Many
- **Special Features**: Hierarchical categories, Multi-images, SEO, Scraping

### Users App
- **Migrations**: 5 total
- **Models**: 4 (VendorProfile, BuyerProfile, SellerAd, Supplier)
- **Extends**: Django User model
- **Features**: Role-based profiles, Advertising, Supplier management

### Blog App
- **Migrations**: 2 total
- **Models**: 3 (BlogPost, BlogCategory, BlogComment)
- **Features**: Rich text, SEO, Comments, Categories

### Orders App
- **Migrations**: 1 total
- **Models**: 2 (Order, OrderItem)
- **Features**: Order tracking, Status management

---

## 🎯 Future Migration Plans

### Planned Enhancements
- [ ] Add product variants (size, color, etc.)
- [ ] Inventory tracking per variant
- [ ] Wishlist functionality
- [ ] Product view/click tracking
- [ ] Advanced analytics fields
- [ ] Product comparison fields
- [ ] Multi-currency support
- [ ] Product bundles/packages
- [ ] Discount and promotion models
- [ ] Review verification system

### Database Optimization Plans
- [ ] Add composite indexes
- [ ] Optimize foreign key indexes
- [ ] Add full-text search indexes
- [ ] Partitioning for large tables
- [ ] Archive old data strategy

---

## 🛠️ Troubleshooting Migrations

### Common Issues

#### Issue: Migration conflicts
```bash
# Solution: Merge migrations
python manage.py makemigrations --merge
```

#### Issue: Fake migration (already applied manually)
```bash
# Solution: Fake it
python manage.py migrate --fake products 0024
```

#### Issue: Reset all migrations (DANGER - DEV ONLY)
```bash
# 1. Delete all migration files except __init__.py
# 2. Drop database
docker-compose down -v
# 3. Recreate
docker-compose up -d
python manage.py makemigrations
python manage.py migrate
```

#### Issue: Rollback to specific migration
```bash
# Rollback products app to migration 0020
python manage.py migrate products 0020
```

---

## 📝 Migration Checklist

Before deploying migrations to production:

- [ ] Migrations tested in local environment
- [ ] Database backed up
- [ ] Migration plan reviewed (`migrate --plan`)
- [ ] Data migrations tested with real data
- [ ] Rollback procedure documented
- [ ] No destructive changes without backup
- [ ] Performance impact assessed
- [ ] Downtime estimated (if any)
- [ ] Team notified of migration
- [ ] Monitoring ready for post-migration

---

## 📚 Additional Resources

- Django Migrations: https://docs.djangoproject.com/en/4.2/topics/migrations/
- Migration Operations: https://docs.djangoproject.com/en/4.2/ref/migration-operations/
- Schema Editor: https://docs.djangoproject.com/en/4.2/ref/schema-editor/

---

**Last Updated**: October 27, 2025  
**Current Latest Migration**: products.0023_add_batch_reporting  
**Total Migrations**: 31 across all apps

