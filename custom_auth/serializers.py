from tokenize import TokenError
from rest_framework import serializers
import urllib

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from .utils import Util
from django.conf import settings
from django.template.loader import render_to_string
from .models import SaasUser  # Adjust to your User model

# make instance (object) from the class User
saasuser = SaasUser()

# class saas

# ---------------------------------(login)-------------------------------------
class SaasLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = SaasUser
        fields = ["email", "password", "is_admin"]

# ---------------------------------(user-profile)-------------------------------------


class SaasuserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaasUser
        fields = [
            "id",
            "email",
            "username",
            "is_admin",
            "Age",
            "Gender",
            "Address"

        ]

#----------------------------add_saasUser----------------------------------

class addSaasAdminSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = SaasUser
        fields = [
            "id",
            "email",
            "username",
            "Age",
            "Gender",
            "Address",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "password dont match"})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password2")
        return SaasUser.objects.create_user(**validated_data)


    def create(self, validated_data):
        validated_data["is_admin"] = True
        password = validated_data.pop("password", None)
        validated_data.pop("password2", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
#--------------------------------list admins----------------------
class SaasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaasUser
        fields = ["id", "username", "Age","Gender","Address", "is_admin"]


class SaasUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaasUser
        fields = [
            "id",
            "username",
            "Age","Gender","Address",
            "is_admin",
            "email",
            "password",
        ]

        # password myzhr4
        extra_kwargs = {
            "password": {"write_only": True},
        }
        # to hash the password

    def create(self, validated_data):
        validated_data["is_admin"] = False
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

