from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.
class TenantUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True,blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, choices=[
        ('manager', 'Manager'),
        ('Seller', 'Seller'),
        ('kitchen', 'Kitchen'),
        ('delivery', 'Delivery'),
    ], default='user')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Tenant User"
        verbose_name_plural = "Tenant Users"
