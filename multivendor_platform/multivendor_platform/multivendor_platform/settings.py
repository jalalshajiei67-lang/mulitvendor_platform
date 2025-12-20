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
    'payments',  # Payment processing
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this at the top
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files in production
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
            'CONN_MAX_AGE': 60,
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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Collected static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Source static files directory
]

# WhiteNoise configuration for serving static files in production
# Using ManifestStaticFilesStorage - WhiteNoise will handle compression on-the-fly
STATICFILES_STORAGE = 'whitenoise.storage.ManifestStaticFilesStorage'

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

# CORS settings - read from environment or use defaults
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'

if not CORS_ALLOW_ALL_ORIGINS:
    # Parse CORS origins from environment
    cors_origins_str = os.environ.get('CORS_ALLOWED_ORIGINS', '')
    if cors_origins_str:
        CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',') if origin.strip()]
    else:
        CORS_ALLOWED_ORIGINS = [
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",  # Nuxt dev server
            "http://127.0.0.1:3000",  # Nuxt dev server
        ]
        if DEBUG:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("CORS_ALLOW_ALL_ORIGINS is False but CORS_ALLOWED_ORIGINS is not set. Using default localhost origins.")
else:
    CORS_ALLOWED_ORIGINS = []
    if DEBUG:
        print("[CORS] Allowing all origins (CORS_ALLOW_ALL_ORIGINS=True)")

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
    'x-guest-session-id',
    'access-control-request-method',  # Required for preflight requests
    'access-control-request-headers',  # Required for preflight requests
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
# Expose headers that frontend might need
CORS_EXPOSE_HEADERS = [
    'content-type',
    'x-total-count',
    'x-page-count',
]
# Cache preflight requests for 1 hour
CORS_PREFLIGHT_MAX_AGE = 3600

# CORS Expose Headers - Headers that can be accessed by the frontend
CORS_EXPOSE_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
    'x-guest-session-id',
]

# CORS Preflight Max Age - Cache preflight requests for 1 hour (3600 seconds)
CORS_PREFLIGHT_MAX_AGE = 3600

# CORS URL Regex - Only apply CORS to API endpoints
CORS_URLS_REGEX = r'^/api/.*$'

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

# Security settings for production behind reverse proxy (nginx/Traefik)
# This ensures Django correctly builds HTTPS URLs when behind a proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_TLS = os.environ.get('USE_TLS', 'False') == 'True'
if USE_TLS:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Configure DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'multivendor_platform.authentication.CsrfExemptSessionAuthentication',  # Custom session auth without CSRF
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

# OTP Configuration
OTP_SENDER_CLASS = os.environ.get('OTP_SENDER_CLASS', 'users.services.otp_senders.LocalOTPSender')
OTP_EXPIRATION_MINUTES = int(os.environ.get('OTP_EXPIRATION_MINUTES', '5'))
OTP_RATE_LIMIT_REQUESTS = int(os.environ.get('OTP_RATE_LIMIT_REQUESTS', '3'))
OTP_RATE_LIMIT_WINDOW_MINUTES = int(os.environ.get('OTP_RATE_LIMIT_WINDOW_MINUTES', '15'))

# Channels Configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

# Build Redis connection string
if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [REDIS_URL],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [(REDIS_HOST, REDIS_PORT)],
            },
        },
    }

# Fallback to in-memory channel layer for development without Redis
if DEBUG and REDIS_HOST == 'localhost':
    try:
        import redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        r.ping()
    except:
        # Redis not available, use in-memory channel layer
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels.layers.InMemoryChannelLayer'
            }
        }
