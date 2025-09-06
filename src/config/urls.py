# Main URL configuration for VLE User Management System
# Decision: Centralized URL routing with feature-based organization

from django.contrib import admin
from django.urls import path, include
from django.conf import settings

# Core URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.v1.urls')),
]

# Development-specific URLs
# Decision: Only include debug toolbar in development to avoid security issues
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns