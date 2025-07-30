from django.urls import path, include
from . import views
urlpatterns = [
    path('clients/',views.ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<id>/', views.ClientDetailView.as_view(), name='get_client-detail'),
    path('branches/', views.BranchListCreateView.as_view(), name='branch-list-create'),
    path('branches/<int:pk>/', views.BranchDetailView.as_view(), name='branch-detail'),
]