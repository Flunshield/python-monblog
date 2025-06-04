# Settings pour le build Docker - pas de base de données requise
from .settings import *

# Désactiver la base de données pour le build
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Désactiver les middlewares qui nécessitent la DB
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Désactiver le logging vers fichiers
LOGGING['handlers'] = {
    'console': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'formatter': 'simple',
    },
}

LOGGING['loggers'] = {
    'django': {
        'handlers': ['console'],
        'level': 'WARNING',
        'propagate': False,
    },
}

# Variables statiques pour le build
SECRET_KEY = 'build-only-secret-key-not-for-production'
ALLOWED_HOSTS = ['*']
DEBUG = False

# Désactiver les vérifications de sécurité pour le build
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
