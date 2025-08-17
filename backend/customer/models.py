from django.db import models

# Create your models here.

class Customer (models.Model):
    customer_neme = models.CharField(max_length=100)
    customer_email = models.EmailField(max_length=100)
    customer_phone = models.IntegerField()
    customer_address = models.CharField(max_length=100)
    customer_BD = models.DateField(blank = True)
    connect_way = models.CharField(max_length=100,blank = True)
    status = models.CharField(max_length=100,blank = True)
    VIP = models.BooleanField(default= False,blank = True)
    notes = models.TextField(blank = True)
    def __str__ (self):
        return self.customer_name
    

