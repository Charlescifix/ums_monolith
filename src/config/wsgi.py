# WSGI config for VLE User Management System
# Decision: Standard Django WSGI configuration with environment variable support

import os
from django.core.wsgi import get_wsgi_application

# Set default settings module
# Decision: Use development settings as default, override in production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

application = get_wsgi_application()