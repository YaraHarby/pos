from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 
from .models import Customer,InvoiceItem,Invoice,Returns_of_customer
from . import serializers
from tenantusers.permissions import IsSeller
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, generics,permissions
from tenantusers.authentication import TenantJWTAuthentication
from rest_framework import viewsets
from sales.serializers import OrderSerializer,OrderItemSerializer
from sales.models import Order,OrderItem
from rest_framework.decorators import action

class customerCreateListView(generics.ListCreateAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Customer.objects.all()
    serializer_class = serializers.customerSerializers
    permission_classes = [IsAuthenticated, IsSeller]
    def perform_create(self, serializer):
        serializer.save()
        return [IsAuthenticated(), IsSeller()]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()

class customerDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Customer.objects.all()
    serializer_class = serializers.customerSerializers
    permission_classes = [IsAuthenticated, IsSeller]
    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "PUT"}:
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()



class InvoiceCreateListView(generics.ListCreateAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    def perform_create(self, serializer):
        serializer.save()
        return [IsAuthenticated(), IsSeller()]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()
    
class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "PUT","DELETE"}:
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()
    

class ReturnCreateListView(generics.ListCreateAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Returns_of_customer.objects.all()
    serializer_class = serializers.ReturnSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    def perform_create(self, serializer):
        serializer.save()
        return [IsAuthenticated(), IsSeller()]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()
    
class ReturnDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TenantJWTAuthentication]
    queryset = Returns_of_customer.objects.all()
    serializer_class = serializers.ReturnSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "PUT","DELETE"}:
            return [IsAuthenticated(), IsSeller()]
        return super().get_permissions()


