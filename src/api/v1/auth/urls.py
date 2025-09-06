# Authentication API URLs
# Decision: Clear, RESTful URL patterns

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='auth-register'),
    path('login/', views.login, name='auth-login'),
    path('password-reset/', views.password_reset, name='auth-password-reset'),
]