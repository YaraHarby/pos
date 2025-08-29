from django.shortcuts import render
from rest_framework import status, generics,permissions
from rest_framework.decorators import api_view ,permission_classes
from . import serializers
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .import serializers 
from .models import SaasUser, RefreshTokenStore
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from tenantusers.models import TenantUser
from tenantusers.serializers import TenantUserSerializer
from django_tenants.utils import schema_context
from tenantusers.models import TenantUser
from django.contrib.auth.hashers import check_password
from tenants.models import Tenant
from django.contrib.auth.hashers import make_password

# ----------------
# Create your views here.
# ----------------------(jwt_tokens)-------------------------------------------------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


#-------------------(login)-------------------------------------------------

@api_view(["POST"])
def Saaslogin(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"msg": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = SaasUser.objects.get(email=email)
    except SaasUser.DoesNotExist:
        return Response({"msg": "Invalid SaaS credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if check_password(password, user.password):
        token = get_tokens_for_user(user)
        return Response({"token": token, "msg": "SaaS login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"msg": "Invalid SaaS credentials"}, status=status.HTTP_401_UNAUTHORIZED)




        
# ----------------------(logout Saas_user _view)-------------------------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh_token = request.data.get("refresh_token")


    if not refresh_token:
        return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

    deleted, _ = RefreshTokenStore.objects.filter(token=refresh_token).delete()
    if deleted:


        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
  
    return Response({"detail": "No matching refresh token found"}, status=status.HTTP_404_NOT_FOUND)

# ----------------------(userprofile_view)-------------------------------------------------

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated,permissions.IsAdminUser])
def saasprofile(request):
    if request.method == "GET":
        serializer = serializers.SaasuserProfileSerializer(
            request.user, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

# ----------------------(addadmin)-------------------------------------------------

class add_saasadmin(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    def post(self, request):
        if not request.user.is_admin:
            return Response({"message": "Don't have access"}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.addSaasAdminSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)
    
# ------------------------------(list_all_saas_admin)---------------------------------------

class listadmins(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        serializerr = serializers.SaasuserProfileSerializer(request.user)
        if serializerr.data["is_admin"] == False:
            return Response({"message": "Don't have access"})

        user = SaasUser.objects.all()
        if not user:
            return Response({"message": "There is no users"},status = status.HTTP_204_NO_CONTENT)

        serializer = serializers.SaasSerializer(user, many=True, context={"request": request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    
#-------------------------------------(get_saasuser)-----------------------------------
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated,permissions.IsAdminUser])
def get_saasuser(request,id):
    if request.method == "GET":
        serializer = serializers.SaasuserProfileSerializer(request.user)
        if serializer.data["is_admin"] == False:
            return Response({"message": "Don't have access"})
        user = SaasUser.objects.filter(id=id).first()
        if not user is None:
            serializer = serializers.SaasUserSerializer(user, context={"request": request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message": "user not found"},status=status.HTTP_400_BAD_REQUEST)
#------------------------------(update_user)--------------------------
@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def update_user(request, id):
    if request.method == "PATCH":

        if not request.user.is_admin:
            return Response({"message": "Don't have access"}, status=status.HTTP_403_FORBIDDEN)
        user = SaasUser.objects.filter(id=id).first()
        if user:
            serializer = serializers.SaasUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#--------------------------------(delete_user)--------------------------------
@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated,permissions.IsAdminUser])
def delete_user(request,id):
    if not request.user.is_admin:
        return Response({"message": "Don't have access"}, status=status.HTTP_403_FORBIDDEN)

    serializer = serializers.SaasuserProfileSerializer(request.user)
    if serializer.data["is_admin"] == False:
        return Response({"message": "Don't have access"},status=status.HTTP_202_ACCEPTED )
    user = SaasUser.objects.filter(id=id).first()
    if user:
        user.delete()
        return Response({"message": "deleted succesfully"},status =status.HTTP_204_NO_CONTENT)
    return Response({"message": "user not found"},status = status.HTTP_400_BAD_REQUEST)

        
    
#--------------------------------------------(delete_myaccount)----------------------------------------

@api_view(["DELETE"])
def delete_account(request):
    try:
        user = request.user
        user.delete()
        return Response(
            {"msg": "Account deleted successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"msg": "Failed to delete account"}, status=status.HTTP_400_BAD_REQUEST
        )


# ------------------------------------------------------------------------------------------
# -------------------------------(user_update_profile)-------------------------------------------
@api_view(["GET", "PUT"])
def update_profile(request):
    if request.method == "GET":
        serializer = serializers.SaasSerializer(
            request.user, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        count = 0
        existing_data = serializers.SaasSerializer(
            request.user, context={"request": request}).data
        y = existing_data.values()
        y = list(y)
        print(type(y))
        print(y)

        serializer = serializers.SaasSerializer(
            request.user, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            x = serializer.data.values()
            keys = serializer.data.keys()
            keys = list(keys)
            x = list(x)
            print(type(x))
            print(x)
            ls = []
            for i in range(5):
                if y[i] == x[i]:
                    continue
                else:
                    ls.append(f"{keys[i]} updated successfully")
                    count += 1
            if count == 0:
                return Response(
                    {"msg": "No changes made"}, status=status.HTTP_406_NOT_ACCEPTABLE
                )
            return Response({"msg": ls}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------------


class CreateTenantUserFromSaaS(APIView):
    def post(self, request, *args, **kwargs):
        schema_name = request.data.get("schema") 
        if not schema_name:
            return Response({"error": "schema is required"}, status=400)

        try:
            with schema_context(schema_name):
                # Get the tenant instance
                tenant = Tenant.objects.get(schema_name=schema_name)

                if tenant.no_users > 0:
                    # Decrement allowed user count
                    tenant.no_users -= 1
                    tenant.save(update_fields=["no_users"])

                    user = TenantUser.objects.create(
                        username=request.data["username"],
                        email=request.data["email"],
                        password=make_password(request.data["password"]), 
                        role=request.data.get("role", "user"),
                        is_active=True,
                    )
                    return Response({"status": "created", "id": user.id}, status=201)
                else: 
                    return Response({"error": "number of users is exceeded"}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)



