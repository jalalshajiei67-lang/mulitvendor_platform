# CapRover Production Settings
import os
import logging
from pathlib import Path
from django.templatetags.static import static

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS for CapRover production
allowed_hosts_str = os.environ.get('ALLOWED_HOSTS', 'multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]

# CSRF Trusted Origins - Required for production HTTPS
csrf_trusted_origins_str = os.environ.get('CSRF_TRUSTED_ORIGINS', 
    'https://multivendor-backend.indexo.ir,https://indexo.ir,https://www.indexo.ir')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_trusted_origins_str.split(',') if origin.strip()]

# Application definition
INSTALLED_APPS = [
    'daphne',  # ASGI server for Channels (must be at top)
    'unfold',  # Modern admin theme - must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',  # For automatic sitemap generation

    # Third-party apps
    'channels',  # WebSocket support
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
    'pages',
    'gamification',
    'chat',  # Chat system
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # MUST be at the top - handles OPTIONS preflight
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
ASGI_APPLICATION = 'multivendor_platform.asgi.application'

# Database configuration for CapRover PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your-strong-password'),
        'HOST': os.environ.get('DB_HOST', 'srv-captain--multivendor-db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Redis configuration for Channels (WebSocket chat)
REDIS_HOST = os.environ.get('REDIS_HOST', 'srv-captain--multivendor-redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')  # CapRover Redis usually doesn't need password

# Channel layers configuration for WebSocket support
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
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

# Base URL for building absolute URLs (used in serializers)
BASE_URL = os.environ.get('BASE_URL', 'https://multivendor-backend.indexo.ir')

# Site URL for SEO (robots.txt, sitemap, canonical URLs)
# Used for generating absolute URLs in sitemaps and robots.txt
# Falls back to request if not set
SITE_URL = os.environ.get('SITE_URL', 'https://indexo.ir')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings for CapRover production
# Note: Update these to match your actual frontend and backend URLs
cors_origins_str = os.environ.get('CORS_ALLOWED_ORIGINS', 'https://indexo.ir,https://www.indexo.ir,https://multivendor-backend.indexo.ir')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',') if origin.strip()]

# Additional CORS settings for production
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'False').lower() == 'true'

# CORS headers and methods - explicitly allow all necessary headers
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
    'access-control-request-method',
    'access-control-request-headers',
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
    'access-control-allow-origin',
    'access-control-allow-credentials',
]

# Preflight cache duration (in seconds) - 24 hours
CORS_PREFLIGHT_MAX_AGE = 86400

# Allow all origins for preflight (django-cors-headers handles this automatically)
# This ensures OPTIONS requests are handled correctly
CORS_URLS_REGEX = r'^/api/.*$'  # Only apply CORS to API endpoints

# Configure DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Allow public read access to API
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ]
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

# Proxy SSL header - Required for Django to detect HTTPS when behind CapRover proxy
# CapRover sets X-Forwarded-Proto header, so Django knows the original request was HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie security settings for HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Logging configuration
# Try to use file logging if logs directory is writable, otherwise use console only
_logs_dir = '/app/logs'
_logs_file = os.path.join(_logs_dir, 'django.log')

# Check if logs directory exists and is writable
_use_file_logging = False
try:
    os.makedirs(_logs_dir, exist_ok=True)
    # Test write access
    test_file = os.path.join(_logs_dir, '.test_write')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    _use_file_logging = True
except (OSError, PermissionError):
    # If we can't write to logs directory, use console only
    _use_file_logging = False

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
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Add file handler only if directory is writable
if _use_file_logging:
    LOGGING['handlers']['file'] = {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'filename': _logs_file,
        'formatter': 'verbose',
    }
    LOGGING['root']['handlers'].append('file')
    LOGGING['loggers']['django']['handlers'].append('file')
