# serializers.py
from rest_framework import serializers
from .models import TenantUser,Branch


class AddTenantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = [
            "id",
            "email",
            "username",
            "role",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_role(self, value):
        # خذ الـ tenant من request
        tenant = getattr(self.context['request'], 'tenant', None)
        if not tenant:
            raise serializers.ValidationError("Tenant not found.")

        # Manager و Seller مسموح لهم دائمًا
        if value in ["Manager", "Seller"]:
            return value

        # تحقق من modules_enabled
        modules_enabled = tenant.modules_enabled or {}
        role_map = {
            "kitchen": "kitchen",
            "Delivery": "Delivery"
        }

        module_key = role_map.get(value)
        if module_key and not modules_enabled.get(module_key, False):
            raise serializers.ValidationError(f"Tenant does not allow adding users with role '{value}'.")

        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance




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


class TenantUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)

class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "contact_email",
            "contact_phone",
        ]
