# API v1 URL routing
# Decision: Organize URLs by feature for better maintainability

from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.v1.auth.urls')),
    path('users/', include('api.v1.users.urls')),
]