from django.urls import path, include
from . import views
urlpatterns = [
    path('tenantusers/', views.TenantUsercreatelistView.as_view(), name='tenant_users_list'),
    path('tenantusers/<int:pk>/', views.TenantUserDetailView.as_view(), name='tenant_user_detail'),
    path('branches/', views.branchCreateListView.as_view(), name='branch_list_create'),
    path('branches/<int:pk>/', views.branchDetailView.as_view(), name='branch_detail'),
    path('login/', views.login ,name = 'login'),
    path('addbranch/',views.add_branch_for_tenant)
    
]