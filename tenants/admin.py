from django.contrib import admin



# Register your models here.

from .models import Tenant, Domain, Client



@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("arabic_name", "End_Date", "on_trial","is_active","Activity_Type")


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("domain", "tenant", "is_primary")


admin.site.register(Client)

# class TenantAdminSite(admin.AdminSite):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.register (Tenant)
#         self.register (Domain)
#         self.register (Client)

# Tenant_admin_site = TenantAdminSite(name='tenant_admin_site')



