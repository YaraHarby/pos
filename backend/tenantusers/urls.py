from django.urls import path, include
from . import views
urlpatterns = [
    path('tenantusers/', views.TenantUsercreatelistView.as_view(), name='tenant_users_list'),
    
]