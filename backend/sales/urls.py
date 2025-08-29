from django.urls import path, include
from . import views
urlpatterns = [
    
    path('products/',views.ProductCreateListView.as_view()),
    path('products/<int:pk>/',views.productDetailView.as_view()),
    path('orders/',views.orderCreateListView.as_view()),
    path('orders/<int:pk>/',views.orderDetailView.as_view()),
    path('receipts/',views.Receiptcraetelistview.as_view()),
    path('receipts/<int:pk>/',views.receiptDetailView.as_view()),
    path('suppliers/',views.suppliercraetelistview.as_view()),
    path('suppliers/<int:pk>/',views.supplierDetailView.as_view()),
   



]