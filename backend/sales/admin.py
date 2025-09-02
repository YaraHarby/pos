from django.contrib import admin
from .models import Product,Voucher,Supplier,Order,OrderItem,Receipt,Invoice,InvoiceItem,Supplier,PurchaseOrder,PurchaseOrderItem,Returns_of_supplier
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Receipt)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Returns_of_supplier)
admin.site.register(Voucher)





 