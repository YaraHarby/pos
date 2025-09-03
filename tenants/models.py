from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from datetime import timedelta
from django.utils import timezone


def default_extra_data():
    """
    Default values for enabled modules in a tenant.
    """
    return {
        "kitchen": False,
        "Delivery": False,
    }


class Tenant(TenantMixin):
    arabic_name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100, blank=True)
    Commercial_Record = models.IntegerField()
    Activity_Type = models.CharField(max_length=50, blank=True)
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
    no_branches = models.IntegerField(default=1)

    auto_create_schema = True

    def __str__(self):
        return self.arabic_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def check_and_deactivate(self):
        """
        Deactivates the tenant if the trial period or subscription has ended.
        """
        today = timezone.now().date()

        # Trial expiration check
        if self.on_trial and self.Start_Date and (self.Start_Date + timedelta(days=14) < today):
            self.is_active = False
            self.save(update_fields=["is_active"])

        # Subscription expiration check
        elif not self.on_trial and self.End_Date and self.End_Date < today:
            self.is_active = False
            self.save(update_fields=["is_active"])


class Domain(DomainMixin):
    """
    Domain model for linking subdomains to tenants.
    """
    pass


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



    
