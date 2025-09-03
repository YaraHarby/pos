from django.urls import path, include
from . import views
urlpatterns = [
    path('tenants/', views.TenantListCreateView.as_view(), name='tenant-list-create'),
    path('tenants/<int:pk>/', views.TenantDetailView.as_view(), name='tenant-detail'),
    path('clients/',views.ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='get_client-detail'),
    path('domains/', views.DominListCreateView.as_view(), name='domain-list-create'),

    

]