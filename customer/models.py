from django.db import models
from sales.models import OrderItem,Product,Order
# Create your models here.

class Customer (models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(max_length=100)
    customer_phone = models.IntegerField()
    customer_address = models.CharField(max_length=100)
    customer_BD = models.DateField(blank = True,null=True)
    connect_way = models.CharField(max_length=100,blank = True)
    status = models.CharField(max_length=100,choices=[('active','Active'),('inactive','InActive')],blank = True)
    VIP = models.BooleanField(default= False,blank = True)
    notes = models.TextField(blank = True)
    def __str__ (self):
        return self.customer_name


    
class Invoice (models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,blank = True, null = True)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(auto_now_add=True)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=30)
    notes = models.TextField(blank = True)
    def __str__ (self):
        return f'{self.customer_name} {self.issue_date} {self.due_date}'

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    
class Returns_of_customer (models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem,on_delete = models.CASCADE)
    quantity = models.IntegerField()
    return_reason = models.CharField(max_length=255)
    description = models.TextField(blank =True)
    created_at = models.DateTimeField(auto_now_add=True,blank = True, null = True)
    


