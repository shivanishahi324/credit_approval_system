from pathlib import Path
import os
import dj_database_url

# -------------------- BASE DIR --------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------- SECURITY --------------------
SECRET_KEY = 'django-insecure-ql=&=4=mv1$(omuh2=dnv8@z=4b$2g8iglo5-c#+z@*5cqai&a'
DEBUG = False  # For production
ALLOWED_HOSTS = [
    'credit-approval-system-26fb.onrender.com',
    'www.credit-approval-system-26fb.onrender.com',
    '127.0.0.1',
    'localhost'
]

# -------------------- CSRF & SECURITY FIXES --------------------
CSRF_TRUSTED_ORIGINS = [
    'https://credit-approval-system-26fb.onrender.com',
    'https://www.credit-approval-system-26fb.onrender.com',
]

# Render ke proxy ke liye fix
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Some Render setups need this:
CSRF_TRUSTED_ORIGINS += ['https://' + host for host in ALLOWED_HOSTS if '.' in host]

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
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------- URLS & TEMPLATES --------------------
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

# -------------------- DATABASE (POSTGRES ON RENDER) --------------------
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
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# -------------------- DEFAULT PRIMARY KEY --------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------- CELERY CONFIG (OPTIONAL) --------------------
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
