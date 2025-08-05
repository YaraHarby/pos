from django.core.management.base import BaseCommand
from tenants.models import Tenant

class Command(BaseCommand):
    help = 'Deactivate tenants whose subscriptions have expired.'

    def handle(self, *args, **kwargs):
        tenants = Tenant.objects.filter(is_active=True)
        for tenant in tenants:
            tenant.check_and_deactivate()
        self.stdout.write(self.style.SUCCESS("Checked and deactivated expired tenants."))