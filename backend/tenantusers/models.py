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
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Tenant User"
        verbose_name_plural = "Tenant Users"


class tenRefreshTokenStore(models.Model):
    user = models.ForeignKey(TenantUser, on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token[:10]}"
    

class Branch(models.Model):
    name = models.CharField(max_length=255)

    contact_email = models.EmailField(blank=True)
    contact_phone = models.IntegerField(blank=True)

    def __str__(self) -> str:  
        return f"{self.name}"