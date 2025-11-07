# CapRover Production Settings
import os
from pathlib import Path
from django.templatetags.static import static

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS for CapRover production
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir').split(',')

# CSRF Trusted Origins - Required for production HTTPS
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 
    'https://multivendor-backend.indexo.ir,https://indexo.ir,https://www.indexo.ir').split(',')

# Application definition
INSTALLED_APPS = [
    'unfold',  # Modern admin theme - must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',  # For automatic sitemap generation

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',  # For token authentication
    'corsheaders',  # To allow requests from your Vue frontend
    'django_filters',
    'tinymce',  # Rich text editor for admin

    # Your apps
    'users',
    'products',
    'orders',
    'blog',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required for admin
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for admin
    'django.contrib.messages.middleware.MessageMiddleware',  # Required for admin
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'multivendor_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'multivendor_platform.wsgi.application'

# Database configuration for CapRover PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', 'multivendor_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^'),
        'HOST': os.environ.get('DB_HOST', 'srv-captain--postgres-db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) for CapRover
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATIC_ROOT = os.environ.get('STATIC_ROOT', '/app/staticfiles')  # Different from source directory

# STATICFILES_DIRS - where Django looks for additional static files before collectstatic
# Include project-level static directory (for custom admin CSS/JS)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Static files finders - tells Django where to look for static files
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files (user uploaded content) for CapRover
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/app/media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings for CapRover production
# Note: Update these to match your actual frontend and backend URLs
cors_origins_str = os.environ.get('CORS_ALLOWED_ORIGINS', 'https://indexo.ir,https://www.indexo.ir,https://multivendor-backend.indexo.ir')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',') if origin.strip()]

# Additional CORS settings for production
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'False').lower() == 'true'

# CORS headers and methods
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Expose headers to frontend
CORS_EXPOSE_HEADERS = [
    'content-type',
    'authorization',
]

# Preflight cache duration (in seconds)
CORS_PREFLIGHT_MAX_AGE = 86400

# Configure DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # GET requests allowed without auth
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Unfold Admin Configuration  
UNFOLD = {
    "SITE_TITLE": "Multivendor Admin",
    "SITE_HEADER": "Product Management System",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("icon-light.svg"),
        "dark": lambda request: static("icon-dark.svg"),
    },
    "SHOW_HISTORY": True,  # Show history button
    "SHOW_VIEW_ON_SITE": True,  # Show view on site button  
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "🛍️ Products Management",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Products",
                        "icon": "shopping_bag",
                        "link": lambda request: "/admin/products/product/",
                        "badge": lambda request: "primary",
                    },
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": lambda request: "/admin/products/category/",
                    },
                    {
                        "title": "Subcategories",
                        "icon": "account_tree",
                        "link": lambda request: "/admin/products/subcategory/",
                    },
                    {
                        "title": "Departments",
                        "icon": "store",
                        "link": lambda request: "/admin/products/department/",
                    },
                    {
                        "title": "Product Images",
                        "icon": "image",
                        "link": lambda request: "/admin/products/productimage/",
                    },
                    {
                        "title": "Product Comments",
                        "icon": "comment",
                        "link": lambda request: "/admin/products/productcomment/",
                    },
                ],
            },
            {
                "title": "🤖 Scraping Tools",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "📋 Batch Scraper",
                        "icon": "rocket_launch",
                        "link": lambda request: "/admin/products/productscrapejob/add-scrape-jobs/",
                        "badge": lambda request: "⭐ START HERE",
                    },
                    {
                        "title": "Scrape Jobs",
                        "icon": "task",
                        "link": lambda request: "/admin/products/productscrapejob/",
                    },
                    {
                        "title": "Scrape Batches",
                        "icon": "inventory_2",
                        "link": lambda request: "/admin/products/scrapejobatch/",
                    },
                ],
            },
            {
                "title": "👥 Users & Vendors",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": lambda request: "/admin/auth/user/",
                    },
                    {
                        "title": "Suppliers",
                        "icon": "business",
                        "link": lambda request: "/admin/users/supplier/",
                    },
                    {
                        "title": "Vendor Profiles",
                        "icon": "badge",
                        "link": lambda request: "/admin/users/vendorprofile/",
                    },
                    {
                        "title": "User Profiles",
                        "icon": "account_circle",
                        "link": lambda request: "/admin/users/userprofile/",
                    },
                ],
            },
            {
                "title": "📝 Blog & Content",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Blog Posts",
                        "icon": "article",
                        "link": lambda request: "/admin/blog/blogpost/",
                    },
                    {
                        "title": "Blog Categories",
                        "icon": "label",
                        "link": lambda request: "/admin/blog/blogcategory/",
                    },
                    {
                        "title": "Blog Comments",
                        "icon": "chat",
                        "link": lambda request: "/admin/blog/blogcomment/",
                    },
                ],
            },
            {
                "title": "📦 Orders",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Orders",
                        "icon": "receipt",
                        "link": lambda request: "/admin/orders/order/",
                    },
                    {
                        "title": "Order Items",
                        "icon": "list_alt",
                        "link": lambda request: "/admin/orders/orderitem/",
                    },
                ],
            },
        ],
    },
    "COLORS": {
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
            "950": "23 37 84",
        },
    },
}

# TinyMCE Configuration
TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
            save link image media preview codesample contextmenu
            table code lists fullscreen insertdatetime nonbreaking
            directionality searchreplace wordcount visualblocks
            visualchars autolink charmap print hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | h1 h2 h3 h4 |
            fontselect, fontsizeselect | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor | code | ltr rtl
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
    'directionality': 'rtl',  # Right-to-left for Persian/Farsi
    'language': 'fa',  # Persian language
    'content_css': [
        '//fonts.googleapis.com/css?family=Vazir',  # Persian font
    ],
    'font_formats': 'Vazir=vazir,sans-serif;Arial=arial,helvetica,sans-serif;Arial Black=arial black,avant garde;Book Antiqua=book antiqua,palatino;Comic Sans MS=comic sans ms,sans-serif;Courier New=courier new,courier;Georgia=georgia,palatino;Helvetica=helvetica;Impact=impact,chicago;Symbol=symbol;Tahoma=tahoma,arial,helvetica,sans-serif;Terminal=terminal,monaco;Times New Roman=times new roman,times;Trebuchet MS=trebuchet ms,geneva;Verdana=verdana,geneva;Webdings=webdings;Wingdings=wingdings,zapf dingbats',
    'table_default_styles': {
        'border': '1px solid #ccc',
        'borderCollapse': 'collapse'
    },
    'table_default_attributes': {
        'border': '1'
    },
    'paste_data_images': True,
    'extended_valid_elements': 'table[*],tr[*],td[*],th[*]',
    'block_formats': 'Paragraph=p; Header 1=h1; Header 2=h2; Header 3=h3; Header 4=h4; Header 5=h5; Header 6=h6; Preformatted=pre',
}

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookie security settings for HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/app/logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
