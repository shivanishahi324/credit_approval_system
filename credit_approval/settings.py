from pathlib import Path
import os
import dj_database_url

# -------------------- BASE DIR --------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------- SECURITY --------------------
SECRET_KEY = 'django-insecure-ql=&=4=mv1$(omuh2=dnv8@z=4b$2g8iglo5-c#+z@*5cqai&a'

# 🔥 LOCAL DEVELOPMENT → DEBUG ON
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "credit-approval-system-26fb.onrender.com",
    ".onrender.com"
]

CSRF_TRUSTED_ORIGINS = [
    "https://credit-approval-system-26fb.onrender.com"
]

# Render proxy fix (safe)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Secure cookies (Render ke liye), LOCAL me allowed hai
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# ❌ LOCAL me HTTPS redirect nahi karega
# SECURE_SSL_REDIRECT = True  # DISABLED for local run

# CSRF Debug view
CSRF_FAILURE_VIEW = "credit_approval.views.csrf_debug_view"

# -------------------- APPLICATIONS --------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'customers',
    'loans',
    'django_extensions',
]

# -------------------- MIDDLEWARE --------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'credit_approval.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'credit_approval' / 'templates'],
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

WSGI_APPLICATION = 'credit_approval.wsgi.application'

# ----------------------------------------------------
#                DATABASE CONFIG
# ----------------------------------------------------
if os.environ.get("DOCKER_ENV") == "true":
    print(" Using LOCAL Docker PostgreSQL")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get("POSTGRES_DB", "credit_approval_db"),
            'USER': os.environ.get("POSTGRES_USER", "postgres"),
            'PASSWORD': os.environ.get("POSTGRES_PASSWORD", "postgres"),
            'HOST': os.environ.get("POSTGRES_HOST", "db"),
            'PORT': '5432',
        }
    }

else:
    print(" Using REMOTE Render PostgreSQL")

    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get(
                'DATABASE_URL',
                'postgresql://credit_approval_db_user:WM8b1S7hRpck7ytdp4IKFTvmXL6vt3fO@dpg-d3tsg8k9c44c73e9eug0-a.oregon-postgres.render.com/credit_approval_db'
            ),
            conn_max_age=600,
            ssl_require=True
        )
    }

# -------------------- PASSWORD VALIDATION --------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------- INTERNATIONALIZATION --------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------- STATIC FILES --------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []

# -------------------- DEFAULT PRIMARY KEY --------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------- CELERY CONFIG (OPTIONAL) --------------------
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# -------------------- DRF Browsable API ENABLE --------------------
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}
