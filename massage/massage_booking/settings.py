import os
from pathlib import Path

# ======================== БАЗОВЫЕ НАСТРОЙКИ ========================

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-%5%$lji9tjp-v-)6*b=!*#7m-uvg=bl*f06wr$*7c$b%v-_)u&'
DEBUG = True
ALLOWED_HOSTS = []

# ======================== ПРИЛОЖЕНИЯ ========================

INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонние
    'import_export',

    # Локальные
    'home',
    'booking',
    'store',
    'services',
    'users',
    'orders',
]

# ======================== MIDDLEWARE ========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======================== URLS / WSGI ========================

ROOT_URLCONF = 'massage_booking.urls'
WSGI_APPLICATION = 'massage_booking.wsgi.application'

# ======================== TEMPLATES ========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Корневая директория шаблонов
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ======================== БАЗА ДАННЫХ ========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ======================== ВАЛИДАЦИЯ ПАРОЛЕЙ ========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ======================== ЛОКАЛИЗАЦИЯ ========================

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ======================== ФАЙЛЫ ========================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ======================== СЕССИИ ========================

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 дней
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ======================== EMAIL ========================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-relay.brevo.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "9295c3001@smtp-brevo.com"
EMAIL_HOST_PASSWORD = "ySPDZw54CFrmKQI2"
DEFAULT_FROM_EMAIL = "danila.medvedkovo21@gmail.com"

# ======================== ПРОЧЕЕ ========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
FILE_CHARSET = 'utf-8'
DEFAULT_CHARSET = 'utf-8'
