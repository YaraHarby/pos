from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.postgres.fields import ArrayField  # Add this import at the top if not already present


class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    subscription_plan = models.CharField(max_length=50, default="basic")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    domain = models.CharField(max_length=255, blank=True)
    subdomain = models.CharField(max_length=255, blank=True)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=50, default="manager")
    modules_enabled = ArrayField(
        base_field=models.CharField(max_length=30),
        default=list,
        blank=True,
        help_text="List of enabled modules like 'kitchen', 'reports', etc."
    )

    def __str__(self):
        return self.name
    
    
class Domain(DomainMixin):
    """Domain model mapping hostnames to tenants."""

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

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.tenant.name} - {self.name}"