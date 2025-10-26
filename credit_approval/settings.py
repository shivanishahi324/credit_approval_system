from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

#  SECURITY
SECRET_KEY = 'django-insecure-ql=&=4=mv1$(omuh2=dnv8@z=4b$2g8iglo5-c#+z@*5cqai&a'
DEBUG = False  #  For production on Render

#  HOSTS & CSRF FIXES
ALLOWED_HOSTS = [
    'credit-approval-system-26fb.onrender.com',
    'www.credit-approval-system-26fb.onrender.com',
    '127.0.0.1',
    'localhost'
]

CSRF_TRUSTED_ORIGINS = [
    'https://credit-approval-system-26fb.onrender.com',
    'https://www.credit-approval-system-26fb.onrender.com',
]

# ✅ HTTPS / Proxy header (Render reverse proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# ✅ (Optional) Allow cross-origin POSTs if using external API
CSRF_COOKIE_DOMAIN = 'credit-approval-system-26fb.onrender.com'

# ✅ Apps
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

# ✅ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'credit_approval.urls'

# ✅ Templates
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

# ✅ Database (Render PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get(
            'DATABASE_URL',
            'postgresql://credit_approval_db_user:WM8b1S7hRpck7ytdp4IKFTvmXL6vt3fO@dpg-d3tsg8k9c44c73e9eug0-a.oregon-postgres.render.com/credit_approval_db'
        ),
        conn_max_age=600,  # better performance
        ssl_require=True
    )
}

# ✅ Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ✅ Default primary key field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ Celery (optional local use)
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
