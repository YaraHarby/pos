from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import TenantUser

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