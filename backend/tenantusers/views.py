from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 
from .models import TenantUser
from . import serializers
from .permissions import IsManager
from rest_framework_simplejwt.tokens import RefreshToken
from . models import TenantUser, tenRefreshTokenStore
from rest_framework.response import Response
from rest_framework import status, generics,permissions
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view ,permission_classes
from django.contrib.auth.hashers import check_password
from .authentication import TenantJWTAuthentication
from .models import Branch
from tenants.models import Tenant








# Create your views here.
# manager views


# ----------------------(jwt_tokens)-------------------------------------------------
# views.py

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
#-----------------------------------(login)--------------------------------------------------------
@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:

        return Response({"msg": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = TenantUser.objects.get(email=email)
        print(user)
    except TenantUser.DoesNotExist:
        print("one")
        return Response({"msg": "Invalid Tenant credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    print(password==user.password)
    if password==user.password:
        print("three")
        token = get_tokens_for_user(user)

        # Remove old refresh tokens
        tenRefreshTokenStore.objects.filter(user=user).delete()
        tenRefreshTokenStore.objects.create(user=user, token=token["refresh"])

        return Response({"token": token, "msg": "Tenant login successful"}, status=status.HTTP_200_OK)
    else:
        print("two")
        return Response({"msg": "Invalid Tenant credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#-------------------------------------(create , list users)-------------------------------------------------------------------
class TenantUsercreatelistView(generics.ListCreateAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = TenantUser.objects.all()
    serializer_class = serializers.TenantUserSerializer
    def get_permissions(self):
        if self.request.method == "POST":
            tenant = Tenant()
            if tenant.no_users > 0:

                tenant.no_users -= 1
                tenant.save(update_fields=["no_users"])
                return [IsAuthenticated(), IsManager()]
            else:
                return Response({"error": "number of users is exceeded"}, status=400)

        if self.request.method == 'GET':
            return [IsAuthenticated(),IsManager()]
        return super().get_permissions()
#-------------------------------------(update , delete users)-------------------------------------------------------------------
    
class TenantUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = TenantUser.objects.all()
    serializer_class = serializers.TenantUserSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "DELETE", "PUT"}:
            return [IsAuthenticated(), IsManager()]
        return super().get_permissions()
    

  
    
#-------------------------------------(create , list branches)-------------------------------------------------------------------
    
class branchCreateListView(generics.ListCreateAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Branch.objects.all()
    serializer_class = serializers.BranchSerializer
    
    permission_classes = [IsAuthenticated, IsManager]

    def get_permissions(self):
        if self.request.method == "POST":
            tenant = Tenant()
            if tenant.no_branches > 0:

                tenant.no_branches -= 1
                tenant.save(update_fields=["no_branches"])
                return [IsAuthenticated(), IsManager()]
            else:
                return Response({"error": "number of branches is exceeded"}, status=400)
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsManager()]
        return super().get_permissions()
#-------------------------------------(update , delete branches)-------------------------------------------------------------------

class branchDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Branch.objects.all()
    serializer_class = serializers.BranchSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "DELETE", "PUT"}:
            return [IsAuthenticated(), IsManager()]
        return super().get_permissions()
    


from django_tenants.utils import schema_context
from tenants.models import Tenant

@api_view(["POST"])
def add_branch_for_tenant(request):
    # 1. أضف بيانات الفرع الجديد داخل tenant schema الحالي
    branch = Branch.objects.create(
        name=request.data["name"],
        contact_email = request.data["contact_email"],
        contact_phone = request.data["contact_phone"]
    )

    # 2. حدّث عدد الفروع في جدول Tenant داخل public schema
    current_schema = connection.schema_name
    with schema_context('public'):
        tenant = Tenant.objects.get(schema_name=current_schema)
        tenant.no_branches += 1
        tenant.save(update_fields=["no_branches"])

    return Response({"message": "تم إضافة الفرع بنجاح"})
