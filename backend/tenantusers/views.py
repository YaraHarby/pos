from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from .models import TenantUser
from .serializers import TenantUserSerializer
from .permissions import IsManager, IsAdminorManager


# Create your views here.

class TenantUsercreatelistView(generics.ListCreateAPIView):
    queryset = TenantUser.objects.all()
    serializer_class = TenantUserSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminorManager()]
        return super().get_permissions()
    