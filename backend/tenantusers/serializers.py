from rest_framework import serializers
from .models import TenantUser
class TenantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ['id', 'username', 'email', 'password', 'role', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = TenantUser(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'user'),
            is_active=validated_data.get('is_active', True)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    