# multivendor_platform/settings.py
import os
from pathlib import Path

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
    'daphne',  # ASGI server for Channels (must be at top)
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
    'payments',  # Payment management
    'sms_newsletter',  # SMS newsletter for sellers
    'auctions',  # Reverse auctions
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be at the top for CORS
    'pages.middleware.RedirectMiddleware',  # Handle manual redirects from admin
    'multivendor_platform.robots_middleware.BackendRobotsNoIndexMiddleware',  # Block indexing on backend domains
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required for admin
    'django.middleware.common.CommonMiddleware',
    'multivendor_platform.csrf_exempt_middleware.CsrfExemptApiMiddleware',  # Exempt API routes from CSRF
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for admin
    'django.contrib.messages.middleware.MessageMiddleware',  # Required for admin
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================================
# Request/Response Timeout Settings (for robustness under pressure)
# ============================================================

# Data upload settings - prevent memory exhaustion from large uploads
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get('DATA_UPLOAD_MAX_MEMORY_SIZE', 10485760))  # 10MB default
DATA_UPLOAD_MAX_NUMBER_FIELDS = int(os.environ.get('DATA_UPLOAD_MAX_NUMBER_FIELDS', 1000))  # Prevent field flooding

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get('FILE_UPLOAD_MAX_MEMORY_SIZE', 10485760))  # 10MB in memory
FILE_UPLOAD_PERMISSIONS = 0o644  # Uploaded files are readable by owner and group

# Connection timeouts are handled at the server level (Daphne/Gunicorn)

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
            # Connection pooling - keep connections alive for reuse
            'CONN_MAX_AGE': int(os.environ.get('DB_CONN_MAX_AGE', '600')),  # 10 minutes default
            # Connection health checks
            'CONN_HEALTH_CHECKS': True,  # Django 4.1+ - test connections before use
            # Additional PostgreSQL-specific options for robustness
            'OPTIONS': {
                'connect_timeout': int(os.environ.get('DB_CONNECT_TIMEOUT', '10')),  # Connection timeout in seconds
                'options': '-c statement_timeout=30000',  # 30 second query timeout
                'keepalives': 1,
                'keepalives_idle': 30,  # Send keepalive after 30 seconds of inactivity
                'keepalives_interval': 10,  # Resend keepalive every 10 seconds
                'keepalives_count': 5,  # Drop connection after 5 failed keepalives
            },
            # Atomic requests - wrap each request in a transaction
            'ATOMIC_REQUESTS': False,  # Set to True if you want automatic transaction management
            # Test database settings
            'TEST': {
                'NAME': 'test_multivendor_db',
            },
        }
    }
else:
    # SQLite for local development without Docker
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'CONN_MAX_AGE': 0,  # Disable connection pooling for SQLite
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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Collected static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Source static files directory
]

# WhiteNoise configuration for serving static files in production
# Using custom storage class that ignores missing source map files
# This prevents collectstatic from failing on missing .map files
STATICFILES_STORAGE = 'multivendor_platform.storage.IgnoreMissingSourceMapsStorage'

# Media files (user uploaded content)
# Use an absolute URL in production if the PUBLIC_MEDIA_URL env var is set,
# otherwise, fall back to the relative '/media/' for local development.
MEDIA_URL = os.getenv('PUBLIC_MEDIA_URL', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Site URL for SEO (robots.txt, sitemap, canonical URLs)
# Used for generating absolute URLs in sitemaps and robots.txt
# This should point to the FRONTEND (Nuxt) URL, not the Django backend
# Falls back to request if not set
# Development example: 'http://localhost:3000'
# Production example: 'https://indexo.ir'
SITE_URL = os.environ.get('SITE_URL', '')  # e.g., 'https://indexo.ir' or 'http://localhost:3000'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# CORS Configuration - Enhanced for Production Under Pressure
# ============================================================

# Remove deprecated CORS_REPLACE_HTTPS_REFERER setting if it exists
# This setting was removed in django-cors-headers 4.0+
if 'CORS_REPLACE_HTTPS_REFERER' in os.environ:
    del os.environ['CORS_REPLACE_HTTPS_REFERER']

# CORS settings - read from environment or use defaults
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'

# Important: In production, set CORS_ALLOW_ALL_ORIGINS=False and specify allowed origins
if not CORS_ALLOW_ALL_ORIGINS:
    # Parse CORS origins from environment
    cors_origins_str = os.environ.get('CORS_ALLOWED_ORIGINS', '')
    if cors_origins_str:
        CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',') if origin.strip()]
        # Debug: Log CORS origins in development
        if DEBUG:
            print(f"[CORS] Allowed origins: {CORS_ALLOWED_ORIGINS}")
    else:
        # Default development origins
        CORS_ALLOWED_ORIGINS = [
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",  # Nuxt dev server
            "http://127.0.0.1:3000",  # Nuxt dev server
        ]
else:
    CORS_ALLOWED_ORIGINS = []
    if DEBUG:
        print("[CORS] ⚠️  WARNING: Allowing all origins (CORS_ALLOW_ALL_ORIGINS=True)")
        print("[CORS] This should ONLY be used in development!")

# Allow credentials (cookies, authorization headers) in CORS requests
CORS_ALLOW_CREDENTIALS = True

# Comprehensive list of allowed headers for CORS requests
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'accept-language',
    'authorization',
    'content-type',
    'content-length',
    'dnt',
    'origin',
    'referer',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-guest-session-id',
    'cache-control',
    'pragma',
    'if-modified-since',
    'if-none-match',
    # Required for preflight requests
    'access-control-request-method',
    'access-control-request-headers',
]

# HTTP methods allowed for CORS requests
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'HEAD',  # Added HEAD for health checks
]

# Headers that can be accessed by the frontend (expose to JavaScript)
CORS_EXPOSE_HEADERS = [
    'content-type',
    'content-length',
    'authorization',
    'x-csrftoken',
    'x-guest-session-id',
    'etag',
    'cache-control',
    'expires',
    'last-modified',
]

# Cache preflight requests for 24 hours (86400 seconds) to reduce OPTIONS requests
# This significantly improves performance under pressure
CORS_PREFLIGHT_MAX_AGE = int(os.environ.get('CORS_PREFLIGHT_MAX_AGE', '86400'))

# Apply CORS only to API endpoints (not admin, static, media)
# This improves security and performance
CORS_URLS_REGEX = r'^/api/.*$'

# Note: CORS_REPLACE_HTTPS_REFERER was removed in django-cors-headers 4.0+
# This setting is no longer needed or supported

# CSRF Trusted Origins - Required for admin login and API requests from frontend
csrf_trusted_origins_str = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if csrf_trusted_origins_str:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_trusted_origins_str.split(',') if origin.strip()]
else:
    # Default for local development
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",  # Nuxt dev server
        "http://127.0.0.1:3000",  # Nuxt dev server
    ]

# ============================================================
# Security Settings - Enhanced for Production
# ============================================================

# Security settings for production behind reverse proxy (nginx/Traefik)
# This ensures Django correctly builds HTTPS URLs when behind a proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_TLS = os.environ.get('USE_TLS', 'False') == 'True'

if USE_TLS:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # HSTS (HTTP Strict Transport Security) settings
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000'))  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    # Content Security
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    # Referrer Policy
    SECURE_REFERRER_POLICY = 'same-origin'
else:
    # Development settings
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Session configuration - optimize for performance and security
SESSION_ENGINE = os.environ.get('SESSION_ENGINE', 'django.contrib.sessions.backends.db')  # Database-backed sessions
SESSION_COOKIE_NAME = 'multivendor_sessionid'
SESSION_COOKIE_AGE = int(os.environ.get('SESSION_COOKIE_AGE', '1209600'))  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = False  # Only save when modified
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# CSRF configuration
CSRF_COOKIE_NAME = 'multivendor_csrftoken'
CSRF_COOKIE_HTTPONLY = False  # Must be False for JavaScript to read it
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False  # Store CSRF token in cookie, not session
CSRF_COOKIE_AGE = 31449600  # 1 year

# X-Frame-Options - prevent clickjacking
X_FRAME_OPTIONS = 'DENY'

# Additional security headers
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups' if not DEBUG else None

# ============================================================
# Django REST Framework Configuration - Enhanced for Production
# ============================================================
REST_FRAMEWORK = {
    # No default authentication - allows anonymous access to public endpoints
    # Views that need authentication should specify authentication_classes explicitly
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(os.environ.get('DRF_PAGE_SIZE', '10')),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # Throttling - Protect against abuse under pressure
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': os.environ.get('DRF_ANON_RATE', '1000/hour'),  # Anonymous users
        'user': os.environ.get('DRF_USER_RATE', '5000/hour'),  # Authenticated users
    },
    # Renderer configuration - reduce processing overhead
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ] if not DEBUG else [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Only in development
    ],
    # Parser configuration
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    # Content negotiation
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',
    # Metadata
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    # Exception handling
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    # Datetime format
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S.%fZ',
    'DATETIME_INPUT_FORMATS': ['%Y-%m-%dT%H:%M:%S.%fZ', 'iso-8601'],
    # Encoding
    'UNICODE_JSON': True,
    'COMPACT_JSON': not DEBUG,  # Compact JSON in production
    # Coerce decimal to string for JSON serialization
    'COERCE_DECIMAL_TO_STRING': True,
    # Schema generation
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
}

# TinyMCE Configuration
TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': 'advlist,autolink,lists,link,image,charmap,preview,anchor,searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,help,wordcount',
    'toolbar1': 'fullscreen preview bold italic underline | h1 h2 h3 h4 | fontselect fontsizeselect | forecolor backcolor | alignleft alignright aligncenter alignjustify | indent outdent | bullist numlist table | link image media',
    'toolbar2': 'visualblocks | charmap anchor | code | ltr rtl',
    'menubar': True,
    'statusbar': True,
    'directionality': 'rtl',  # Right-to-left for Persian/Farsi
    'language': 'fa',  # Persian language
    'content_css': [
        '/static/admin/css/custom_admin.css',  # Custom Persian font support
    ],
    'font_formats': 'Arial=arial,helvetica,sans-serif;Arial Black=arial black,avant garde;Book Antiqua=book antiqua,palatino;Comic Sans MS=comic sans ms,sans-serif;Courier New=courier new,courier;Georgia=georgia,palatino;Helvetica=helvetica;Impact=impact,chicago;Symbol=symbol;Tahoma=tahoma,arial,helvetica,sans-serif;Terminal=terminal,monaco;Times New Roman=times new roman,times;Trebuchet MS=trebuchet ms,geneva;Verdana=verdana,geneva;Webdings=webdings;Wingdings=wingdings,zapf dingbats',
    'table_default_styles': {
        'border': '1px solid #ccc',
        'borderCollapse': 'collapse'
    },
    'table_default_attributes': {
        'border': '1'
    },
    # Image upload configuration - Direct file picker (no dialog)
    'file_picker_callback': 'tinymceImageFilePicker',  # Custom file picker function
    'file_picker_types': 'image',  # Only show for images
    'images_upload_url': '/tinymce/upload-image/',  # Image upload endpoint
    'images_upload_base_path': '/media/',  # Base path for images
    'images_upload_credentials': True,  # Include credentials in upload request
    'images_reuse_filename': False,  # Generate unique filenames
    'images_file_types': 'jpg,jpeg,png,gif,webp',  # Allowed image types
    'paste_data_images': True,  # Allow pasting images from clipboard
    'image_advtab': False,  # Disable advanced tab (we use direct upload)
    'image_caption': True,  # Enable image captions
    'image_list': False,  # Disable image list
    'image_title': True,  # Enable image title attribute
    'image_dimensions': True,  # Show image dimensions
    'image_class_list': [
        {'title': 'None', 'value': ''},
        {'title': 'Responsive', 'value': 'img-responsive'},
        {'title': 'Rounded', 'value': 'img-rounded'},
        {'title': 'Circle', 'value': 'img-circle'},
        {'title': 'Thumbnail', 'value': 'img-thumbnail'},
    ],
    'image_uploadtab': False,  # Disable upload tab (we use file picker)
    'extended_valid_elements': 'table[*],tr[*],td[*],th[*],img[*]',
    'block_formats': 'Paragraph=p; Header 1=h1; Header 2=h2; Header 3=h3; Header 4=h4; Header 5=h5; Header 6=h6; Preformatted=pre',
    'relative_urls': False,
    'remove_script_host': False,
    'convert_urls': True,
    'browser_spellcheck': True,
    'resize': True,
    'branding': False,
}

# OTP Configuration
OTP_SENDER_CLASS = os.environ.get('OTP_SENDER_CLASS', 'users.services.otp_senders.LocalOTPSender')
OTP_EXPIRATION_MINUTES = int(os.environ.get('OTP_EXPIRATION_MINUTES', '5'))
OTP_RATE_LIMIT_REQUESTS = int(os.environ.get('OTP_RATE_LIMIT_REQUESTS', '3'))
OTP_RATE_LIMIT_WINDOW_MINUTES = int(os.environ.get('OTP_RATE_LIMIT_WINDOW_MINUTES', '15'))

# ============================================================
# Channels Configuration - Enhanced for Production Reliability
# ============================================================
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
REDIS_DB = int(os.environ.get('REDIS_DB', '0'))

# Build Redis connection string with enhanced configuration
if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [REDIS_URL],
                # Connection pool settings for better performance under pressure
                "capacity": int(os.environ.get('REDIS_CHANNEL_CAPACITY', '1000')),  # Max messages per channel
                "expiry": int(os.environ.get('REDIS_CHANNEL_EXPIRY', '60')),  # Message expiry in seconds
                # Connection retry settings
                "channel_capacity": int(os.environ.get('REDIS_CHANNEL_LAYER_CAPACITY', '100')),
                # Symmetric encryption for WebSocket messages (optional)
                "symmetric_encryption_keys": [SECRET_KEY[:32]],  # Use first 32 chars of SECRET_KEY
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [(REDIS_HOST, REDIS_PORT)],
                # Connection pool settings
                "capacity": int(os.environ.get('REDIS_CHANNEL_CAPACITY', '1000')),
                "expiry": int(os.environ.get('REDIS_CHANNEL_EXPIRY', '60')),
                "channel_capacity": int(os.environ.get('REDIS_CHANNEL_LAYER_CAPACITY', '100')),
                # Symmetric encryption
                "symmetric_encryption_keys": [SECRET_KEY[:32]],
            },
        },
    }

# Fallback to in-memory channel layer for development without Redis
if DEBUG and REDIS_HOST == 'localhost':
    try:
        import redis
        r = redis.Redis(
            host=REDIS_HOST, 
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            socket_connect_timeout=5,
            socket_keepalive=True,
            health_check_interval=30,
        )
        r.ping()
        print("[Redis] ✅ Connected successfully")
    except Exception as e:
        print(f"[Redis] ⚠️  Redis not available ({e}), using in-memory channel layer")
        # Redis not available, use in-memory channel layer
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels.layers.InMemoryChannelLayer'
            }
        }

# ============================================================
# Redis Caching Configuration (Optional - for performance)
# ============================================================
# Enable Redis caching for better performance under pressure
USE_REDIS_CACHE = os.environ.get('USE_REDIS_CACHE', 'False') == 'True'

if USE_REDIS_CACHE and REDIS_HOST:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL if REDIS_PASSWORD else f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
            'OPTIONS': {
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': int(os.environ.get('REDIS_MAX_CONNECTIONS', '50')),
                    'retry_on_timeout': True,
                    'health_check_interval': 30,
                },
                'IGNORE_EXCEPTIONS': True,  # Don't fail if Redis is down
            },
            'KEY_PREFIX': 'multivendor',
            'TIMEOUT': 300,  # Default cache timeout (5 minutes)
        }
    }
else:
    # Fallback to local memory cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
            'OPTIONS': {
                'MAX_ENTRIES': 1000,
            }
        }
    }

# Zibal Payment Gateway Settings
ZIBAL_MERCHANT = os.environ.get('ZIBAL_MERCHANT', 'zibal')  # Use 'zibal' for test mode
ZIBAL_API_BASE = 'https://gateway.zibal.ir'
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')

# Kavenegar SMS Settings
KAVENEGAR_API_KEY = os.environ.get('KAVENEGAR_API_KEY', '')
KAVENEGAR_TEMPLATE_NAME = os.environ.get('KAVENEGAR_TEMPLATE_NAME', '')  # For newsletter SMS
KAVENEGAR_OTP_TEMPLATE_NAME = os.environ.get('KAVENEGAR_OTP_TEMPLATE_NAME', '')  # For OTP SMS

# ============================================================
# Logging Configuration - Enhanced for Production Debugging
# ============================================================
# Ensure logs directory exists (create with proper error handling)
try:
    LOGS_DIR = BASE_DIR / 'logs'
    LOGS_DIR.mkdir(exist_ok=True)
    # Test if we can write to the directory
    test_file = LOGS_DIR / '.test'
    test_file.touch()
    test_file.unlink()
    LOGS_AVAILABLE = True
except (OSError, PermissionError):
    # If we can't create/write to logs directory, use console only
    LOGS_AVAILABLE = False
    print("[WARNING] Could not create logs directory, using console logging only")

# Build handlers list dynamically based on availability
LOGGING_HANDLERS = {
    'console': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'formatter': 'simple',
    },
}

# Only add file handlers if logs directory is writable
if LOGS_AVAILABLE:
    LOGGING_HANDLERS.update({
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_errors.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'db_file': {
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'database.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
    })

# Configure logger handlers based on what's available
if LOGS_AVAILABLE:
    DJANGO_HANDLERS = ['console', 'file']
    REQUEST_HANDLERS = ['console', 'error_file']
    DB_HANDLERS = ['db_file']
    SECURITY_HANDLERS = ['error_file']
    APP_HANDLERS = ['console', 'file']
else:
    # Console only if logs directory not available
    DJANGO_HANDLERS = ['console']
    REQUEST_HANDLERS = ['console']
    DB_HANDLERS = ['console']
    SECURITY_HANDLERS = ['console']
    APP_HANDLERS = ['console']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': LOGGING_HANDLERS,
    'loggers': {
        'django': {
            'handlers': DJANGO_HANDLERS,
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': REQUEST_HANDLERS,
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': DB_HANDLERS,
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': SECURITY_HANDLERS,
            'level': 'WARNING',
            'propagate': False,
        },
        'multivendor_platform': {
            'handlers': APP_HANDLERS,
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}