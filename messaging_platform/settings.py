import os
from pathlib import Path
import dj_database_url

# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# مفتاح الأمان (يُفضل وضعه في متغير بيئة على Render)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-m(x8xu413g_0^_dfyrw#)mjc_gn7szcc-kx^*pf9xhabh99gjs')

# وضع التصحيح - اجعله False في Render
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['social-vite.onrender.com', '127.0.0.1', 'localhost', '*']

# التطبيقات المثبتة
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'django.contrib.humanize',
    'social', 
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'messaging_platform.urls'

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

WSGI_APPLICATION = 'messaging_platform.wsgi.application'
ASGI_APPLICATION = 'messaging_platform.asgi.application'

# إعداد قاعدة بيانات Neon (الرابط الذي أرسلته)
NEON_DATABASE_URL = "postgresql://neondb_owner:npg_TR9JWPCDy7rh@ep-twilight-snow-ad502c4s-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', NEON_DATABASE_URL),
        conn_max_age=600,
        ssl_require=True
    )
}

# التحقق من كلمة المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# إعدادات اللغة والوقت
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Africa/Algiers'
USE_I18N = True
USE_TZ = True

# الملفات الثابتة
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# الميديا
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'social.CustomUser'

# إعدادات Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dvp5v8v90',
    'API_KEY': '164434235282213',
    'API_SECRET': 'XbB0r2C0SIn7_28hP-EwQhO4S0A'
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'home'
