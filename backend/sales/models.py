from django.db import models
from django.contrib.postgres.fields import ArrayField
from tenantusers.models import TenantUser
from django.utils import timezone
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
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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
    


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    expected_delivery = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Delivered', 'Delivered'),('Cancelled','Cancelled')],
        default='Pending'
    )
    notes = models.TextField(blank=True, null=True)
    # total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"PO-{self.id} ({self.status})"


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, related_name="items", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"



class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
        ('overdue', 'overdue')
    ]

    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('CreditCard', 'CreditCard'),
        ('Check','Check')
    ]

    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE, related_name="invoices")
    order_id = models.CharField(max_length=100)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, default='Cash')
    notes = models.TextField(blank=True, null=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # percentage %
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_totals(self):
        subtotal = sum(item.quantity * item.unit_price for item in self.items.all())
        total = subtotal + (subtotal * (self.tax / 100))
        self.subtotal = subtotal
        self.total = total
        self.save()

    def __str__(self):
        return f"Invoice #{self.id} - {self.supplier.supplier_name}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.item_name} ({self.quantity}x)"
    
class Returns_of_supplier (models.Model):
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE)
    purchase_item = models.ForeignKey(PurchaseOrderItem,on_delete = models.CASCADE)
    invoice = models.ForeignKey(Invoice,on_delete = models.CASCADE,blank = True, null = True)
    return_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    refund_method = models.CharField(max_length=100, choices=[('Cash', 'Cash'), ('Bank Transfer', 'Bank Transfer'), ('Check', 'Check')], default='Cash')
    quantity = models.IntegerField()
    return_reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,blank = True, null = True)
    notes = models.TextField(blank=True, null=True)


class Voucher(models.Model):
    VOUCHER_TYPES = [
        ('Supplier', 'Supplier Payment'),
        ('Expense', 'Expense Payment'),
    ]

    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Check', 'Check'),
        ('CreditCard', 'CreditCard'),
    ]

    voucher_number = models.CharField(max_length=100, unique=True)
    voucher_type = models.CharField(max_length=20, choices=VOUCHER_TYPES)

    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, default="Cash")

    # Supplier voucher
    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE, null=True, blank=True)

    # Expense voucher
    category = models.CharField(max_length=50, null=True, blank=True)
    recipient = models.CharField(max_length=255, null=True, blank=True)

    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to="vouchers/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voucher_type} Voucher {self.voucher_number} - {self.amount}"



























