from django.contrib import admin

# Register your models here.

from .models import TenantUser
@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_active')
    list_per_page = 20
