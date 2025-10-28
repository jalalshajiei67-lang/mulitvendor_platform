# multivendor_platform/settings.py
import os
from pathlib import Path
from django.templatetags.static import static

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345678')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS - read from environment or use defaults
allowed_hosts_str = os.environ.get("ALLOWED_HOSTS", "")
if allowed_hosts_str:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(",")]
else:
    # Default for development
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']
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



# Database configuration - reads from environment variables (for Docker)
# Falls back to SQLite if no DB_ENGINE is set
DB_ENGINE = os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3')

if DB_ENGINE == 'django.db.backends.postgresql':
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.environ.get('DB_NAME', 'multivendor_db'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    # SQLite for local development without Docker
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

# Media files (user uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings - read from environment or use defaults
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'

if not CORS_ALLOW_ALL_ORIGINS:
    # Parse CORS origins from environment
    cors_origins_str = os.environ.get('CORS_ALLOWED_ORIGINS', '')
    if cors_origins_str:
        CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',')]
    else:
        CORS_ALLOWED_ORIGINS = [
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        
        ]
else:
    CORS_ALLOWED_ORIGINS = []

CORS_ALLOW_CREDENTIALS = True
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

# Configure DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ]
}

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Unfold Admin Configuration
UNFOLD = {
    "SITE_TITLE": "Multivendor Admin",
    "SITE_HEADER": "Product Management System",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("icon-light.svg"),  # Optional
        "dark": lambda request: static("icon-dark.svg"),  # Optional
    },
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
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen insertdatetime nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists charmap print hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect | forecolor backcolor | alignleft alignright |
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
