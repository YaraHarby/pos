from django.urls import path, include
from . import views


urlpatterns = [
    
    path('customers/',views.customerCreateListView.as_view()),
    path('customers/<int:pk>/',views.customerDetailView.as_view()),
    path('invoices/',views.InvoiceCreateListView.as_view()),
    path('invoices/<int:pk>/',views.InvoiceDetailView.as_view()),
    path('returns/',views.ReturnCreateListView.as_view()),
    path('returns/<int:pk>/',views.ReturnDetailView.as_view()),



]