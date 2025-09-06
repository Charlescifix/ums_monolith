# Development settings for VLE User Management System
# Decision: Separate development settings to enable debugging tools
# and developer-friendly configurations without affecting production

from .base import *

# Enable debugging for development
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Developer tools configuration
# Decision: Add debugging tools only in development to avoid performance impact
INTERNAL_IPS = ['127.0.0.1']

if 'django_debug_toolbar' not in INSTALLED_APPS:
    INSTALLED_APPS += ['django_debug_toolbar']

if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in MIDDLEWARE:
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

# Feature flags for development
# Decision: Enable all features in development for testing purposes
ENABLED_FEATURES = {key: True for key in ENABLED_FEATURES.keys()}