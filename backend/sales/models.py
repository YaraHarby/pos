from django.db import models
from django.contrib.postgres.fields import ArrayField
from tenantusers.models import TenantUser
# from customer.models import Customer




class Supplier (models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    supplier_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    contact_person = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    join_date = models.DateField()
    address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    rating = models.IntegerField(default=0)
    payment_terms = models.CharField(max_length=100, default="30 days")
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # auto record creation
    updated_at = models.DateTimeField(auto_now=True)      # auto record update

    def __str__(self):
        return f"{self.supplier_name} ({self.company})"

#-----------------------------------(product)--------------------------------
class Product(models.Model):
    arabic_name = models.CharField(max_length=255,unique=True)
    english_name = models.CharField(max_length=255,unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length = 255 ,choices = [
        ('main course','main course'),
        ('side dish','side dish'),
        ('beverages','beverages'),
        ('desserts','desserts')

    ])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='items/', blank=True)
    product_no = models.IntegerField(blank = True, null=True)
    barcode = models.CharField(max_length=255,blank=True)
    current_stock = models.IntegerField()
    min_stock = models.IntegerField()
    unit_size = models.DecimalField(max_digits=10, decimal_places=2)
    unit_type = models.CharField(max_length=255,choices = [
        ('gram','gram'),
        ('kilogram','kilogram'),
        ('liter','liter'),
        ('mililiter','mililiter'),
        ('piece','piece'),
        ('box','box'),
        ('carton','carton'),
        ('bottle','bottle'),
        ('can','can'),
        ('pack','pack'),

    ])
    status = models.CharField(max_length=255,default='In Stock')
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,blank=True,null=True)
    suspended =  models.BooleanField(blank= True, null = True,default= False)


    def __str__(self):
        return f"{self.arabic_name} {self.price}"
#----------------------------------------------------------------------------------------------


class Order (models.Model):
    customer = models.ForeignKey("customer.Customer", on_delete=models.CASCADE,null = True)
    seller = models.ForeignKey(TenantUser, on_delete=models.CASCADE)

    status = models.CharField(max_length=250,choices=[
        ('pending','pending'),
        ('processing','processing'),
        ('completed','completed'),
        ('cancelled','cancelled')

    ] )
    payment_type = models.CharField(max_length=250,choices=[
        ('cash','cash'),
        ('card','card'),
        ('knet','knet'),
        ('credit','credit')
    ])
    date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.id} --> {self.quantity} x {self.product}"

class Receipt (models.Model):
    type = models.CharField(max_length=30,choices=[('Customer','Customer'),('Other','Other')])
    received_from = models.CharField(max_length=255)
    receipt_number = models.IntegerField(blank = True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymant_way = models.CharField(max_length=30)
    check_no = models.IntegerField(blank = True,null = True)
    on_bank = models.CharField(max_length = 255)
    purpose = models.TextField(blank=True)
    receiver = models.CharField(max_length = 255)
    date = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to="uploads/")































