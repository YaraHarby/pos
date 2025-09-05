from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import TenantUser
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_tenants.utils import get_tenant_model, tenant_context


class TenantJWTAuthentication(JWTAuthentication):
    # Use the same defaults as the parent class
    user_id_field = "id"
    user_id_claim = "user_id"

    def get_user(self, validated_token):
        try:
            user_id = validated_token[self.user_id_claim]
        except KeyError:
            raise InvalidToken("Token contained no recognizable user identification")

        try:
            return TenantUser.objects.get(**{self.user_id_field: user_id})
        except TenantUser.DoesNotExist:
            raise InvalidToken("user_not_found")
        

User = get_user_model()
Tenant = get_tenant_model()

class TenantActiveBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if request is None:
            return None
        
        # Determine the current tenant (assuming django-tenants middleware is used)
        tenant = getattr(request, 'tenant', None)
        if tenant is None:
            return None
        
        # Check if tenant has expired
        if tenant.End_Date and tenant.End_Date < timezone.now().date():
            return None  # Tenant expired, reject login

        # Normal user authentication
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None
