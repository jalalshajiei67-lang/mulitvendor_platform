# 📡 Complete API Reference

**Comprehensive API documentation for the Multivendor Platform**

---

## 📋 Base Information

```
Base URL:        /api/
Protocol:        HTTP/HTTPS
Format:          JSON
Authentication:  Token-based + Session
Pagination:      10 items per page (default)
```

---

## 🔐 Authentication

### Login
```
POST /api/auth/login/
```

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response 200**:
```json
{
  "token": "string",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "buyer|seller|admin"
  }
}
```

---

### Register
```
POST /api/auth/register/
```

**Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "password_confirm": "string",
  "role": "buyer|seller"
}
```

**Response 201**:
```json
{
  "token": "string",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string"
  }
}
```

---

### Logout
```
POST /api/auth/logout/
```

**Headers**: `Authorization: Token <token>`

**Response 200**:
```json
{
  "detail": "Successfully logged out"
}
```

---

### Get Current User
```
GET /api/auth/me/
```

**Headers**: `Authorization: Token <token>`

**Response 200**:
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "buyer|seller|admin",
  "profile": {
    // Profile data based on role
  }
}
```

---

### Update Profile
```
PUT /api/auth/profile/update/
PATCH /api/auth/profile/update/
```

**Headers**: 
- `Authorization: Token <token>`
- `Content-Type: multipart/form-data` (if uploading images)

**Request Body** (multipart/form-data):
```
first_name: string
last_name: string
email: string
phone: string
avatar: file (optional)
```

**Response 200**:
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  // Updated profile data
}
```

---

## 🛍️ Products

### List Products
```
GET /api/products/
```

**Query Parameters**:
- `page` (integer): Page number (default: 1)
- `search` (string): Search in name and description
- `category` (integer): Filter by category ID
- `subcategory` (integer): Filter by subcategory ID
- `department` (integer): Filter by department ID
- `min_price` (decimal): Minimum price
- `max_price` (decimal): Maximum price
- `ordering` (string): Sort by field (e.g., `price`, `-created_at`)

**Example**:
```
GET /api/products/?page=1&search=laptop&min_price=500&max_price=2000
```

**Response 200**:
```json
{
  "count": 100,
  "next": "http://example.com/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Gaming Laptop",
      "slug": "gaming-laptop-asus-rog",
      "description": "High performance gaming laptop",
      "price": "1499.99",
      "stock_quantity": 10,
      "main_image": "http://example.com/media/products/laptop.jpg",
      "images": [
        {
          "id": 1,
          "image": "http://example.com/media/products/laptop1.jpg",
          "alt_text": "Front view",
          "order": 1
        }
      ],
      "category": {
        "id": 1,
        "name": "Computers",
        "slug": "computers"
      },
      "subcategories": [
        {
          "id": 1,
          "name": "Laptops",
          "slug": "laptops"
        }
      ],
      "vendor": {
        "id": 1,
        "username": "techstore",
        "company_name": "Tech Store Inc"
      },
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-20T14:22:00Z"
    }
  ]
}
```

---

### Get Product Detail
```
GET /api/products/{id}/
GET /api/products/{slug}/
```

**Response 200**:
```json
{
  "id": 1,
  "name": "Gaming Laptop",
  "slug": "gaming-laptop-asus-rog",
  "description": "High performance gaming laptop",
  "price": "1499.99",
  "stock_quantity": 10,
  "sku": "LAPTOP-001",
  "main_image": "http://example.com/media/products/laptop.jpg",
  "image_alt_text": "ASUS ROG Gaming Laptop",
  "images": [
    {
      "id": 1,
      "image": "http://example.com/media/products/laptop1.jpg",
      "alt_text": "Front view",
      "order": 1
    }
  ],
  "category": {
    "id": 1,
    "name": "Computers",
    "slug": "computers",
    "description": "Computer products"
  },
  "subcategories": [
    {
      "id": 1,
      "name": "Laptops",
      "slug": "laptops"
    }
  ],
  "vendor": {
    "id": 1,
    "username": "techstore",
    "company_name": "Tech Store Inc",
    "logo": "http://example.com/media/vendors/logo.jpg"
  },
  "meta_title": "Buy ASUS ROG Gaming Laptop | Tech Store",
  "meta_description": "High performance gaming laptop...",
  "meta_keywords": "gaming, laptop, asus, rog",
  "canonical_url": "https://example.com/products/gaming-laptop-asus-rog/",
  "schema_markup": "{...}",
  "comments": [
    {
      "id": 1,
      "user": "john_doe",
      "rating": 5,
      "comment": "Excellent product!",
      "created_at": "2025-01-18T09:15:00Z"
    }
  ],
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-20T14:22:00Z"
}
```

---

### Create Product
```
POST /api/products/
```

**Headers**: 
- `Authorization: Token <token>`
- `Content-Type: multipart/form-data`

**Permissions**: Seller or Admin only

**Request Body** (multipart/form-data):
```
name: string (required)
description: string (required)
price: decimal (required)
stock_quantity: integer (required)
category: integer (required, category ID)
subcategories: array of integers (optional)
sku: string (optional)
main_image: file (optional)
images: array of files (optional)
meta_title: string (optional)
meta_description: string (optional)
meta_keywords: string (optional)
```

**Response 201**:
```json
{
  "id": 1,
  "name": "Gaming Laptop",
  "slug": "gaming-laptop-asus-rog",
  // ... full product object
}
```

---

### Update Product
```
PUT /api/products/{id}/
PATCH /api/products/{id}/
```

**Headers**: 
- `Authorization: Token <token>`
- `Content-Type: multipart/form-data`

**Permissions**: Owner or Admin only

**Request Body**: Same as Create (all fields optional for PATCH)

**Response 200**: Full product object

---

### Delete Product
```
DELETE /api/products/{id}/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Owner or Admin only

**Response 204**: No content

---

### Get My Products (Seller)
```
GET /api/products/my_products/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Seller only

**Response 200**: Array of products owned by current seller

---

### Add Product Comment
```
POST /api/products/{id}/comment/
```

**Headers**: `Authorization: Token <token>`

**Request Body**:
```json
{
  "rating": 5,
  "comment": "Excellent product!"
}
```

**Response 201**:
```json
{
  "id": 1,
  "user": "john_doe",
  "rating": 5,
  "comment": "Excellent product!",
  "created_at": "2025-01-18T09:15:00Z"
}
```

---

### Get Product Comments
```
GET /api/products/{id}/comments/
```

**Response 200**: Array of comments

---

### Delete Product Image
```
DELETE /api/products/{product_id}/images/{image_id}/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Product owner or Admin

**Response 204**: No content

---

## 📂 Categories

### List Departments
```
GET /api/departments/
```

**Query Parameters**:
- `search` (string): Search in name
- `slug` (string): Filter by slug

**Response 200**:
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "name": "Electronics",
      "slug": "electronics",
      "description": "Electronic products",
      "image": "http://example.com/media/departments/electronics.jpg",
      "meta_title": "Electronics Department",
      "meta_description": "Browse electronics",
      "meta_keywords": "electronics, gadgets",
      "categories_count": 5
    }
  ]
}
```

---

### Get Department Detail
```
GET /api/departments/{id}/
GET /api/departments/{slug}/
```

**Response 200**: Full department object with categories

---

### List Categories
```
GET /api/categories/
```

**Query Parameters**:
- `department` (integer): Filter by department ID
- `search` (string): Search in name
- `slug` (string): Filter by slug

**Response 200**:
```json
{
  "count": 20,
  "results": [
    {
      "id": 1,
      "name": "Computers",
      "slug": "computers",
      "description": "Computer products",
      "image": "http://example.com/media/categories/computers.jpg",
      "department": {
        "id": 1,
        "name": "Electronics",
        "slug": "electronics"
      },
      "subcategories_count": 3
    }
  ]
}
```

---

### Get Category Detail
```
GET /api/categories/{id}/
GET /api/categories/{slug}/
```

**Response 200**: Full category object with subcategories

---

### List Subcategories
```
GET /api/subcategories/
```

**Query Parameters**:
- `category` (integer): Filter by category ID
- `search` (string): Search in name
- `slug` (string): Filter by slug

**Response 200**:
```json
{
  "count": 30,
  "results": [
    {
      "id": 1,
      "name": "Laptops",
      "slug": "laptops",
      "description": "Laptop computers",
      "image": "http://example.com/media/subcategories/laptops.jpg",
      "category": {
        "id": 1,
        "name": "Computers",
        "slug": "computers"
      },
      "products_count": 50
    }
  ]
}
```

---

### Get Subcategory Detail
```
GET /api/subcategories/{id}/
GET /api/subcategories/{slug}/
```

**Response 200**: Full subcategory object with products

---

### Create/Update/Delete Categories
```
POST   /api/categories/
PUT    /api/categories/{id}/
PATCH  /api/categories/{id}/
DELETE /api/categories/{id}/
```

**Permissions**: Admin only

Similar patterns for departments and subcategories.

---

## 📝 Blog

### List Blog Posts
```
GET /api/blog/posts/
```

**Query Parameters**:
- `page` (integer): Page number
- `search` (string): Search in title and content
- `category` (string): Filter by category slug
- `author` (integer): Filter by author ID
- `featured` (boolean): Filter featured posts

**Response 200**:
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "title": "10 Best Laptops for 2025",
      "slug": "10-best-laptops-2025",
      "excerpt": "Discover the top laptops...",
      "featured_image": "http://example.com/media/blog/laptops.jpg",
      "author": {
        "id": 1,
        "username": "admin",
        "full_name": "Admin User"
      },
      "category": {
        "id": 1,
        "name": "Tech Reviews",
        "slug": "tech-reviews"
      },
      "view_count": 1500,
      "is_featured": true,
      "published_at": "2025-01-10T08:00:00Z",
      "created_at": "2025-01-09T15:30:00Z"
    }
  ]
}
```

---

### Get Blog Post Detail
```
GET /api/blog/posts/{slug}/
```

**Response 200**:
```json
{
  "id": 1,
  "title": "10 Best Laptops for 2025",
  "slug": "10-best-laptops-2025",
  "content": "<p>Full HTML content...</p>",
  "excerpt": "Discover the top laptops...",
  "featured_image": "http://example.com/media/blog/laptops.jpg",
  "author": {
    "id": 1,
    "username": "admin",
    "full_name": "Admin User",
    "avatar": "http://example.com/media/avatars/admin.jpg"
  },
  "category": {
    "id": 1,
    "name": "Tech Reviews",
    "slug": "tech-reviews",
    "description": "Technology product reviews"
  },
  "tags": ["laptops", "reviews", "technology"],
  "meta_title": "10 Best Laptops for 2025 | Tech Blog",
  "meta_description": "Comprehensive review of the best laptops...",
  "meta_keywords": "laptops, 2025, best, reviews",
  "canonical_url": "https://example.com/blog/10-best-laptops-2025/",
  "view_count": 1500,
  "is_featured": true,
  "comments": [
    {
      "id": 1,
      "user": "john_doe",
      "comment": "Great article!",
      "created_at": "2025-01-11T10:20:00Z"
    }
  ],
  "published_at": "2025-01-10T08:00:00Z",
  "created_at": "2025-01-09T15:30:00Z",
  "updated_at": "2025-01-10T07:55:00Z"
}
```

---

### Create Blog Post
```
POST /api/blog/posts/
```

**Headers**: 
- `Authorization: Token <token>`
- `Content-Type: multipart/form-data`

**Permissions**: Admin only

**Request Body**:
```
title: string (required)
content: string (required)
excerpt: string (optional)
category: integer (required, category ID)
featured_image: file (optional)
tags: array of strings (optional)
is_featured: boolean (optional)
meta_title: string (optional)
meta_description: string (optional)
```

**Response 201**: Full blog post object

---

### Update Blog Post
```
PUT /api/blog/posts/{slug}/
PATCH /api/blog/posts/{slug}/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Author or Admin

**Request Body**: Same as Create

**Response 200**: Full blog post object

---

### Delete Blog Post
```
DELETE /api/blog/posts/{slug}/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Author or Admin

**Response 204**: No content

---

### Get My Blog Posts
```
GET /api/blog/my-posts/
```

**Headers**: `Authorization: Token <token>`

**Response 200**: Array of posts by current user

---

### Featured Blog Posts
```
GET /api/blog/posts/featured/
```

**Response 200**: Array of featured posts (limit 5)

---

### Recent Blog Posts
```
GET /api/blog/posts/recent/
```

**Response 200**: Array of recent posts (limit 10)

---

### Popular Blog Posts
```
GET /api/blog/posts/popular/
```

**Response 200**: Array of popular posts sorted by view_count (limit 10)

---

### Related Blog Posts
```
GET /api/blog/posts/{slug}/related/
```

**Response 200**: Array of related posts (same category, limit 5)

---

### List Blog Categories
```
GET /api/blog/categories/
```

**Response 200**:
```json
[
  {
    "id": 1,
    "name": "Tech Reviews",
    "slug": "tech-reviews",
    "description": "Technology product reviews",
    "posts_count": 15
  }
]
```

---

### Get Blog Category Detail
```
GET /api/blog/categories/{slug}/
```

**Response 200**: Full category object

---

### Get Category Posts
```
GET /api/blog/categories/{slug}/posts/
```

**Response 200**: Paginated list of posts in category

---

### Add Blog Comment
```
POST /api/blog/posts/{slug}/comment/
```

**Headers**: `Authorization: Token <token>`

**Request Body**:
```json
{
  "comment": "Great article!"
}
```

**Response 201**:
```json
{
  "id": 1,
  "user": "john_doe",
  "comment": "Great article!",
  "created_at": "2025-01-11T10:20:00Z"
}
```

---

### Get Blog Post Comments
```
GET /api/blog/posts/{slug}/comments/
```

**Response 200**: Array of comments

---

## 🔍 Global Search

### Search Everything
```
GET /api/search/
```

**Query Parameters**:
- `q` (string, required): Search query
- `limit` (integer, optional): Results per type (default: 10)

**Response 200**:
```json
{
  "products": [
    {
      "id": 1,
      "name": "Gaming Laptop",
      "slug": "gaming-laptop",
      "price": "1499.99",
      "image": "..."
    }
  ],
  "blog_posts": [
    {
      "id": 1,
      "title": "Laptop Review",
      "slug": "laptop-review",
      "excerpt": "..."
    }
  ],
  "categories": [
    {
      "id": 1,
      "name": "Laptops",
      "slug": "laptops",
      "type": "subcategory"
    }
  ]
}
```

---

## 👤 User Dashboards

### Buyer Dashboard
```
GET /api/auth/buyer/dashboard/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Buyer only

**Response 200**:
```json
{
  "total_orders": 15,
  "pending_orders": 2,
  "total_spent": "5499.95",
  "recent_orders": [...],
  "wishlist_count": 8,
  "recent_reviews": [...]
}
```

---

### Buyer Orders
```
GET /api/auth/buyer/orders/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Buyer only

**Response 200**: Paginated list of buyer's orders

---

### Seller Dashboard
```
GET /api/auth/seller/dashboard/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Seller only

**Response 200**:
```json
{
  "total_products": 25,
  "active_products": 20,
  "total_sales": 150,
  "total_revenue": "45000.00",
  "pending_orders": 5,
  "recent_orders": [...],
  "top_products": [...]
}
```

---

### Seller Orders
```
GET /api/auth/seller/orders/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Seller only

**Response 200**: Paginated list of orders for seller's products

---

### Admin Dashboard
```
GET /api/auth/admin/dashboard/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Admin only

**Response 200**:
```json
{
  "total_users": 500,
  "total_products": 1000,
  "total_orders": 2500,
  "total_revenue": "150000.00",
  "new_users_today": 5,
  "orders_today": 12,
  "recent_activities": [...]
}
```

---

## 📢 Seller Ads

### List Seller Ads
```
GET /api/auth/ads/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Seller only

**Response 200**: Array of seller's ads

---

### Create Seller Ad
```
POST /api/auth/ads/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Seller only

**Request Body**:
```json
{
  "title": "Summer Sale!",
  "description": "50% off all products",
  "link_url": "/products/summer-sale",
  "start_date": "2025-06-01",
  "end_date": "2025-08-31"
}
```

**Response 201**: Full ad object

---

### Update Seller Ad
```
PUT /api/auth/ads/{id}/
PATCH /api/auth/ads/{id}/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Ad owner only

**Request Body**: Same as Create

**Response 200**: Full ad object

---

### Delete Seller Ad
```
DELETE /api/auth/ads/{id}/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Ad owner only

**Response 204**: No content

---

### Upload Ad Image
```
POST /api/auth/ads/{id}/upload_image/
```

**Headers**: 
- `Authorization: Token <token>`
- `Content-Type: multipart/form-data`

**Request Body**:
```
image: file (required)
```

**Response 200**:
```json
{
  "id": 1,
  "image": "http://example.com/media/ads/summer-sale.jpg"
}
```

---

## 👨‍💼 Admin User Management

### List Users
```
GET /api/auth/admin/users/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Admin only

**Query Parameters**:
- `role` (string): Filter by role
- `is_active` (boolean): Filter by active status
- `search` (string): Search username/email

**Response 200**: Paginated list of users

---

### Block User
```
POST /api/auth/admin/users/{id}/block/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Admin only

**Request Body**:
```json
{
  "is_blocked": true
}
```

**Response 200**:
```json
{
  "id": 1,
  "username": "john_doe",
  "is_blocked": true
}
```

---

### Verify User
```
POST /api/auth/admin/users/{id}/verify/
```

**Headers**: `Authorization: Token <token>`

**Permissions**: Admin only

**Request Body**:
```json
{
  "is_verified": true
}
```

**Response 200**:
```json
{
  "id": 1,
  "username": "john_doe",
  "is_verified": true
}
```

---

## 🗺️ Sitemaps

### XML Sitemap
```
GET /sitemap.xml
```

**Response 200**: XML sitemap with all public URLs

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input",
  "details": {
    "field_name": ["Error message"]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

---

## 📊 Rate Limiting

**Current Status**: Not implemented  
**Future**: 100 requests per minute per user

---

## 🔒 Authentication Header Format

All authenticated requests must include:

```
Authorization: Token <your-token-here>
```

Example:
```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
     https://api.example.com/api/products/
```

---

## 📝 Notes

1. **Pagination**: Most list endpoints return paginated results
2. **Slugs**: Can often be used instead of IDs for SEO-friendly URLs
3. **File Uploads**: Use `multipart/form-data` content type
4. **Timestamps**: All timestamps are in ISO 8601 format (UTC)
5. **Soft Deletes**: Some models may use soft deletion
6. **Validation**: All inputs are validated on the backend

---

## 🧪 Testing API Endpoints

### Using cURL
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Get products with token
curl -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8000/api/products/
```

### Using Postman
1. Import API collection (if available)
2. Set base URL: `http://localhost:8000`
3. Add Authorization header with token

### Using Browser
Django REST Framework provides a browsable API:
```
http://localhost:8000/api/
```

---

**Last Updated**: October 27, 2025  
**API Version**: 1.0  
**Status**: Production Ready

