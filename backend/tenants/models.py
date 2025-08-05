from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.postgres.fields import ArrayField  # Add this import at the top if not already present
from datetime import timedelta, date
from django.utils import timezone


def default_extra_data():
    return {
        "kitchen": False,
        "Delivery": False,
    }
class Tenant(TenantMixin):
    arabic_name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100,blank=True)
    Commercial_Record = models.IntegerField()
    Subscription_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Currency = models.CharField(max_length=10, default="SAR")
    subdomain = models.CharField(max_length=255, unique=True)
    Start_Date = models.DateField(auto_now_add=True, blank=True, null=True)
    End_Date = models.DateField(blank=True, null=True)
    on_trial = models.BooleanField(default=True) 
    is_active = models.BooleanField(default=True)  
    no_users = models.IntegerField(default=1) 
    image = models.ImageField(upload_to='tenants/', blank=True, null=True)
    modules_enabled = models.JSONField(default=default_extra_data)

    def __str__(self):
        return self.arabic_name
    
    def save(self, *args, **kwargs):
        if not self.End_Date:
            self.End_Date = self.Start_Date + timedelta(days=14)
        super().save(*args, **kwargs)
    auto_create_schema = True

    def check_and_deactivate(self):
        today = timezone.now().date()
        if self.on_trial and self.Start_Date + timedelta(days=14) < today:
            self.is_active = False
            self.save(update_fields=["is_active"])
        elif not self.on_trial and self.End_Date and self.End_Date < today:
            self.is_active = False
            self.save(update_fields=["is_active"])
        
class Domain(DomainMixin):
    pass


class Branch(models.Model):
    name = models.CharField(max_length=255)
    tenant = models.ForeignKey(
        "tenants.Tenant",
        related_name="branches",
        on_delete=models.CASCADE,
    )
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:  
        return f"{self.tenant.subdomain} - {self.name}"
    

class Client(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        related_name="clients",
        on_delete=models.CASCADE,
    )

    arabic_name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True, blank=True)
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.arabic_name} ({self.tenant.subdomain})"
    


