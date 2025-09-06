# Production settings for VLE User Management System
# Decision: Secure production configuration with Railway optimization

import os
from .base import *
import dj_database_url

# Security settings for production
DEBUG = False
ALLOWED_HOSTS = [
    '.railway.app',
    '.up.railway.app', 
    'localhost',
    '127.0.0.1'
]

# Add custom domain when available
if env('CUSTOM_DOMAIN', default=''):
    ALLOWED_HOSTS.append(env('CUSTOM_DOMAIN'))

# Security middleware for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Use HTTPS in production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Database configuration for Railway
# Railway provides DATABASE_URL automatically
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(
        env('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )

# Static files configuration for Railway
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (if needed)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Email configuration (Railway environment)
if env('EMAIL_HOST', default=''):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env.int('EMAIL_PORT', default=587)
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@example.com')

# Cache configuration (Redis on Railway)
if env('REDIS_URL', default=''):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': env('REDIS_URL'),
        }
    }

# Feature flags can be overridden per deployment
ENABLED_FEATURES.update({
    'role_management': env.bool('ENABLE_ROLES', False),
    'notifications': env.bool('ENABLE_NOTIFICATIONS', False),
    'profile_management': env.bool('ENABLE_PROFILES', False),
    'audit_logging': env.bool('ENABLE_AUDIT', False),
    'two_factor_auth': env.bool('ENABLE_2FA', False),
    'session_management': env.bool('ENABLE_SESSIONS', False),
    'reporting': env.bool('ENABLE_REPORTING', False),
})