# 📊 Multivendor Platform - Visual Project Structure

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULTIVENDOR PLATFORM                         │
│                                                                 │
│  ┌──────────────────────┐         ┌──────────────────────┐    │
│  │   FRONTEND (Vue.js)  │ ◄─────► │  BACKEND (Django)    │    │
│  │   Port: 5173/8080    │  REST   │   Port: 8000         │    │
│  └──────────────────────┘   API   └──────────────────────┘    │
│           │                              │                      │
│           │                              │                      │
│           └──────────┬───────────────────┘                      │
│                      │                                          │
│              ┌───────▼────────┐                                 │
│              │   DATABASE     │                                 │
│              │  PostgreSQL/   │                                 │
│              │    SQLite      │                                 │
│              └────────────────┘                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Directory Structure

```
mulitvendor_platform/
│
├── multivendor_platform/          # Main project directory
│   │
│   ├── multivendor_platform/      # Django Backend
│   │   ├── multivendor_platform/  # Django project settings
│   │   │   ├── settings.py        # Main configuration
│   │   │   ├── urls.py            # Root URL routing
│   │   │   └── wsgi.py            # WSGI config
│   │   │
│   │   ├── users/                 # User Management App
│   │   │   ├── models.py          # User, Profile, Supplier models
│   │   │   ├── views.py           # Auth & user views
│   │   │   ├── serializers.py     # API serializers
│   │   │   └── urls.py            # User API routes
│   │   │
│   │   ├── products/              # Product Management App
│   │   │   ├── models.py          # Product, Category, Department
│   │   │   ├── views.py           # Product views
│   │   │   ├── serializers.py     # Product serializers
│   │   │   ├── scraper.py         # Web scraper
│   │   │   └── urls.py            # Product API routes
│   │   │
│   │   ├── orders/                # Order Management App
│   │   │   ├── models.py          # Order, OrderItem, RFQ
│   │   │   ├── views.py           # Order views
│   │   │   ├── serializers.py     # Order serializers
│   │   │   └── urls.py            # Order API routes
│   │   │
│   │   ├── blog/                  # Blog Management App
│   │   │   ├── models.py          # BlogPost, BlogCategory
│   │   │   ├── views.py           # Blog views
│   │   │   ├── serializers.py     # Blog serializers
│   │   │   └── urls.py            # Blog API routes
│   │   │
│   │   ├── media/                 # User uploaded files
│   │   ├── static/                # Static files
│   │   └── templates/             # Django templates
│   │
│   └── front_end/                 # Vue.js Frontend
│       ├── src/
│       │   ├── views/             # Page components
│       │   ├── components/        # Reusable components
│       │   ├── stores/            # Pinia state management
│       │   ├── services/          # API service layer
│       │   ├── router/            # Vue Router config
│       │   ├── plugins/           # Vuetify, i18n
│       │   └── main.js            # App entry point
│       │
│       ├── package.json           # Frontend dependencies
│       └── vite.config.js         # Vite configuration
│
├── docker-compose.yml             # Docker orchestration
├── Dockerfile                     # Backend container
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## 🔄 Data Flow & Relationships

### Backend Models Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER SYSTEM                             │
└─────────────────────────────────────────────────────────────────┘

    User (Django Auth)
         │
         ├───► UserProfile (role: buyer/seller/both)
         │
         ├───► BuyerProfile (shipping, billing)
         │
         ├───► VendorProfile (store_name, logo, description)
         │
         ├───► Supplier (company info, scraped/manual)
         │
         └───► UserActivity (tracking)

┌─────────────────────────────────────────────────────────────────┐
│                      PRODUCT SYSTEM                             │
└─────────────────────────────────────────────────────────────────┘

    Department
         │
         └───► Category (Many-to-Many)
                    │
                    └───► Subcategory (Many-to-Many)
                               │
                               └───► Product
                                         │
                                         ├───► ProductImage
                                         ├───► ProductReview
                                         └───► Vendor (User)

┌─────────────────────────────────────────────────────────────────┐
│                        ORDER SYSTEM                             │
└─────────────────────────────────────────────────────────────────┘

    Order (buyer, is_rfq)
         │
         ├───► OrderItem (product, quantity, price)
         ├───► OrderImage (for RFQ)
         └───► Payment (transaction)

┌─────────────────────────────────────────────────────────────────┐
│                         BLOG SYSTEM                             │
└─────────────────────────────────────────────────────────────────┘

    BlogCategory
         │
         └───► BlogPost (author, status, featured)
                    │
                    └───► BlogComment (nested replies)
```

---

## 🌐 API Endpoints Structure

```
/api/
│
├── /auth/                        # Authentication & User Management
│   ├── POST   /login/            # User login
│   ├── POST   /register/         # User registration
│   ├── POST   /logout/           # User logout
│   ├── GET    /me/               # Current user info
│   ├── PUT    /profile/update/   # Update profile
│   │
│   ├── /buyer/                   # Buyer endpoints
│   │   ├── GET /dashboard/       # Buyer dashboard
│   │   ├── GET /orders/          # Buyer orders
│   │   └── GET /reviews/         # Buyer reviews
│   │
│   ├── /seller/                  # Seller endpoints
│   │   ├── GET /dashboard/       # Seller dashboard
│   │   ├── GET /orders/          # Seller orders
│   │   └── GET /reviews/         # Seller reviews
│   │
│   └── /admin/                   # Admin endpoints
│       ├── GET  /dashboard/      # Admin dashboard
│       ├── GET  /users/          # User management
│       ├── POST /users/{id}/block/
│       └── GET  /activities/     # Activity logs
│
├── /products/                    # Product Management
│   ├── GET    /                  # List products
│   ├── POST   /                  # Create product
│   ├── GET    /{id}/             # Product detail
│   ├── PUT    /{id}/             # Update product
│   ├── DELETE /{id}/             # Delete product
│   ├── GET    /my_products/      # User's products
│   │
│   ├── /departments/             # Department endpoints
│   ├── /categories/              # Category endpoints
│   └── /subcategories/           # Subcategory endpoints
│
├── /orders/                      # Order Management
│   ├── POST   /rfq/create/       # Create RFQ
│   ├── GET    /vendor/rfq/       # Vendor RFQs
│   └── /admin/rfq/               # Admin RFQ management
│
└── /blog/                        # Blog Management
    ├── GET    /posts/            # List posts
    ├── POST   /posts/            # Create post
    ├── GET    /posts/{slug}/     # Post detail
    ├── PUT    /posts/{slug}/     # Update post
    ├── DELETE /posts/{slug}/     # Delete post
    ├── GET    /categories/       # Blog categories
    └── POST   /posts/{slug}/comment/  # Add comment
```

---

## 🎨 Frontend Architecture

### Vue.js Application Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYERS                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  VIEWS (Pages)                                              │
│  ├── HomeView.vue                                           │
│  ├── ProductList.vue, ProductDetail.vue, ProductForm.vue   │
│  ├── DepartmentList.vue, DepartmentDetail.vue              │
│  ├── CategoryDetail.vue, SubcategoryDetail.vue             │
│  ├── SupplierList.vue, SupplierDetail.vue                  │
│  ├── BlogList.vue, BlogDetail.vue, BlogForm.vue            │
│  ├── LoginView.vue, RegisterView.vue                       │
│  └── BuyerDashboard.vue, SellerDashboard.vue, AdminDashboard.vue │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  COMPONENTS (Reusable UI)                                   │
│  ├── layout/ (Header, Footer, Sidebar)                     │
│  ├── admin/ (Admin-specific components)                    │
│  ├── Breadcrumb.vue                                        │
│  ├── GlobalSearch.vue                                      │
│  ├── RFQForm.vue                                           │
│  └── TiptapEditor.vue                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STORES (Pinia State Management)                            │
│  ├── auth.js (Authentication state)                        │
│  ├── products.js (Product state)                           │
│  └── blog.js (Blog state)                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  SERVICES (API Layer)                                       │
│  └── api.js (Axios client with all API methods)            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PLUGINS                                                    │
│  ├── vuetify (Material Design components)                  │
│  └── i18n (Internationalization - Persian/RTL)             │
└─────────────────────────────────────────────────────────────┘
```

### Frontend Routing Structure

```
/ (Home)
├── /about
├── /contact-us
├── /sitemap
│
├── /login, /register (Auth)
│
├── /departments
│   └── /departments/:slug
│
├── /categories/:slug
├── /subcategories/:slug
│
├── /products
│   ├── /products (List)
│   ├── /products/:id (Detail)
│   ├── /products/new (Create)
│   ├── /products/:id/edit (Edit)
│   └── /my-products (User's products)
│
├── /suppliers
│   ├── /suppliers (List)
│   └── /suppliers/:id (Detail)
│
├── /blog
│   ├── /blog (List)
│   ├── /blog/:slug (Detail)
│   ├── /blog/new (Create)
│   ├── /blog/:slug/edit (Edit)
│   └── /blog/dashboard
│
└── /buyer/dashboard, /seller/dashboard, /admin/dashboard
```

---

## 🔐 User Roles & Permissions

```
┌─────────────────────────────────────────────────────────────┐
│                    USER ROLES                                │
└─────────────────────────────────────────────────────────────┘

    BUYER
    ├── Browse products, categories, suppliers
    ├── Create orders and RFQs
    ├── Write product reviews
    └── Manage own profile

    SELLER (Supplier/Vendor)
    ├── Create and manage products
    ├── View and manage orders
    ├── Create seller advertisements
    ├── Reply to reviews
    └── Manage vendor profile

    ADMIN
    ├── Full system access
    ├── User management (block/verify)
    ├── Product approval/moderation
    ├── Order management
    ├── Blog management
    ├── Category/Department management
    └── Activity monitoring
```

---

## 🗄️ Database Schema Summary

### Core Tables

| Table | Purpose | Key Relationships |
|-------|---------|-------------------|
| `auth_user` | Django user accounts | → UserProfile, VendorProfile |
| `users_userprofile` | Extended user info | → User (1:1) |
| `users_vendorprofile` | Supplier/vendor details | → User (1:1) |
| `users_supplier` | Company/supplier info | → User (M:1) |
| `products_department` | Product departments | → Category (M:M) |
| `products_category` | Product categories | → Department, Subcategory (M:M) |
| `products_subcategory` | Product subcategories | → Category (M:M) |
| `products_product` | Products | → Vendor, Category, Subcategory |
| `products_productimage` | Product images | → Product (M:1) |
| `orders_order` | Orders & RFQs | → Buyer, OrderItem |
| `orders_orderitem` | Order line items | → Order, Product |
| `blog_blogpost` | Blog posts | → Author, BlogCategory |
| `blog_blogcomment` | Blog comments | → BlogPost, Author |

---

## 🔧 Technology Stack

### Backend
- **Framework**: Django 4.x
- **API**: Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Token Authentication + Session Auth
- **Admin**: Django Admin (with TinyMCE)
- **Other**: CORS, WhiteNoise, django-filters

### Frontend
- **Framework**: Vue.js 3 (Composition API)
- **UI Library**: Vuetify 3
- **State Management**: Pinia
- **Routing**: Vue Router 4
- **HTTP Client**: Axios
- **Build Tool**: Vite
- **i18n**: vue-i18n (Persian/RTL support)
- **Rich Text**: Tiptap

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Deployment**: CapRover
- **CI/CD**: GitHub Actions
- **Server**: VPS (185.208.172.76)

---

## 📊 Key Features

### Product Management
- ✅ Hierarchical structure (Department → Category → Subcategory → Product)
- ✅ Multi-image support
- ✅ SEO optimization (meta tags, schema markup)
- ✅ Product scraping from external sources
- ✅ Vendor/supplier management

### Order System
- ✅ Regular orders
- ✅ RFQ (Request for Quotation) system
- ✅ Order tracking
- ✅ Payment integration ready

### User System
- ✅ Multi-role support (Buyer, Seller, Admin)
- ✅ Profile management
- ✅ Activity tracking
- ✅ User verification/blocking

### Blog System
- ✅ Blog posts with categories
- ✅ Rich text editor (Tiptap)
- ✅ Comments system
- ✅ Featured posts

### Admin Features
- ✅ Comprehensive admin dashboard
- ✅ Bulk actions
- ✅ User management
- ✅ Content moderation

---

## 🔄 Request Flow Example

### Product Creation Flow

```
1. User (Seller) → Frontend (ProductForm.vue)
   │
   ▼
2. Frontend → API Service (api.js)
   │  POST /api/products/
   │
   ▼
3. API Service → Django Backend (products/views.py)
   │  ProductCreateView
   │
   ▼
4. Backend → Serializer (products/serializers.py)
   │  ProductSerializer (validation)
   │
   ▼
5. Backend → Model (products/models.py)
   │  Product.save()
   │
   ▼
6. Database → Response
   │
   ▼
7. Backend → Frontend (JSON response)
   │
   ▼
8. Frontend → Store (products.js)
   │  Update state
   │
   ▼
9. UI Update (ProductList.vue)
```

---

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION SETUP                          │
└─────────────────────────────────────────────────────────────┘

    Internet
         │
         ▼
    CapRover (captain.indexo.ir)
         │
         ├───► Backend Container (Django)
         │    ├── Port: 8000
         │    ├── Database: PostgreSQL
         │    └── Static: WhiteNoise
         │
         ├───► Frontend Container (Vue.js)
         │    ├── Port: 5173/8080
         │    └── Build: Vite
         │
         └───► Nginx (Reverse Proxy)
              ├── Static files serving
              └── Media files serving
```

---

## 📝 Notes

- **RTL Support**: Frontend is designed for Persian (RTL) language
- **Mobile First**: UI is designed mobile-first
- **SEO Optimized**: All major models include SEO fields
- **Scraping**: Products can be scraped from external sources
- **RFQ System**: Supports Request for Quotation workflow
- **Multi-vendor**: Supports multiple suppliers/vendors

---

*Last Updated: Generated from project structure analysis*

