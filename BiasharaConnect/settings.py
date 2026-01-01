from pathlib import Path
import os

# --------------------------------------------------
# BASE DIRECTORY
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to your Frontend directory (for local dev/testing)
FRONTEND_DIR = BASE_DIR.parent / 'BiasharaConnectFrontend' / 'public'

# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-#q9yb$hv5hj#$0da5-g@eu%)g@hv!7t+^)@ie_6@$wst3&i2t3'
)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Allowed hosts: include Render backend for production + localhost for dev
ALLOWED_HOSTS = [
    'biashara-connect-backend.onrender.com',  # Render backend
    '127.0.0.1',
    'localhost',
]

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local app
    'BiasharaConnectApp.apps.BiasharaConnectAppConfig',

    # Third-party apps
    'corsheaders',
    'rest_framework',
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # MUST be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------------------------------
# URLS & WSGI
# --------------------------------------------------
ROOT_URLCONF = 'BiasharaConnect.urls'
WSGI_APPLICATION = 'BiasharaConnect.wsgi.application'

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(FRONTEND_DIR)],  # absolute path for dev
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

# --------------------------------------------------
# DATABASE
# --------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    FRONTEND_DIR / 'assets',  # local dev
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # production

# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "https://biashara-connect-frontend.vercel.app",  # frontend on Vercel
    "http://127.0.0.1:5500",                        # local dev
    "http://localhost:5500",
]

CORS_ALLOW_CREDENTIALS = True

# --------------------------------------------------
# DEFAULT AUTO FIELD
# --------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
