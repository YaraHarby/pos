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
    path('purchasess/',views.PurchaseOrderListCreateView.as_view()),
    path('purchasess/<int:pk>/',views.PurchaseDetailView.as_view()),
    path('supinvoices/',views.InvoiceListCreateView.as_view()),
    path('supinvoices/<int:pk>/',views.InvoiceDetailView.as_view()),
    path('returns/',views.ReturnCreateListView.as_view()),
    path('returns/<int:pk>/',views.ReturnDetailView.as_view()),
    path('vouchers/',views.VoucherCreateListView.as_view()),
    path('vouchers/<int:pk>/',views.VoucherDetailView.as_view()),



]