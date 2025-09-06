# User management API URLs

from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user-list'),
    path('<int:user_id>/', views.user_detail, name='user-detail'),
    path('<int:user_id>/update/', views.user_update, name='user-update'),
    path('<int:user_id>/deactivate/', views.user_deactivate, name='user-deactivate'),
    path('bulk/', views.bulk_operations, name='user-bulk-operations'),
]