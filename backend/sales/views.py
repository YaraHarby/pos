from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 
from .models import Product,Supplier,Order,Receipt
from . import serializers
from tenantusers.permissions import IsSeller
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, generics,permissions
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view ,permission_classes
from django.contrib.auth.hashers import check_password
from tenantusers.authentication import TenantJWTAuthentication
from tenants.models import Tenant
from django.db import connection
from django_tenants.utils import schema_context
from rest_framework.views import APIView

class ProductCreateListView(generics.ListCreateAPIView):
    authentication_classes = [TenantJWTAuthentication]
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(suspended=False)

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [IsAuthenticated(), IsSeller()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()
    
#--------------------------------------(product details)----------------------------------------
    
class productDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "PUT"}:
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()


    
#----------------------------------------------------------------------------
#-------------------------------order----------------------------------------------------

class orderCreateListView(generics.ListCreateAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    def perform_create(self, serializer):
        serializer.save()
        return [IsAuthenticated(), IsSeller()]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()

#---------------------------------------------------------------------------------------
class orderDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "PUT"}:
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()

class Receiptcraetelistview(generics.ListCreateAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Receipt.objects.all()
    serializer_class = serializers.ReceiptSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    def perform_create(self, serializer):
        serializer.save()
        return [IsAuthenticated(), IsSeller()]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()
    
class receiptDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Receipt.objects.all()
    serializer_class = serializers.ReceiptSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "PUT"}:
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()

class suppliercraetelistview(generics.ListCreateAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    def perform_create(self, serializer):
        serializer.save()
        return [IsAuthenticated(), IsSeller()]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()
    
class supplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "PUT"}:
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()






