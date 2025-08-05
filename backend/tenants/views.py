from rest_framework import generics, permissions
from rest_framework.decorators import api_view ,permission_classes
from .models import Tenant, Branch, Domain, Client
from . import serializers
from rest_framework.response import Response
# from . permissions import IsManger


class TenantListCreateView(generics.ListCreateAPIView):

    queryset = Tenant.objects.all()
    serializer_class = serializers.TenantSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]
    def get_permissions(self):
        """Allow anonymous POST for new client registration."""
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        if self.request.method == "GET":
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Tenant.objects.all()
    serializer_class = serializers.TenantSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser] 
    
    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "DELETE","PUT"}:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]



class BranchListCreateView(generics.ListCreateAPIView):
    """List branches or create a new one."""

    queryset = Branch.objects.all()
    serializer_class = serializers.BranchSerializer
    permission_classes = [permissions.IsAuthenticated]


class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a branch."""

    queryset = Branch.objects.all()
    serializer_class = serializers.BranchSerializer
    permission_classes = [permissions.IsAuthenticated]

class DominListCreateView(generics.ListCreateAPIView):
    """List domains or create a new one."""

    queryset = Domain.objects.all()
    serializer_class = serializers.DomainSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClientListCreateView(generics.ListCreateAPIView):

    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]
    def get_permissions(self):
        """Allow anonymous POST for new client registration."""
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        if self.request.method == "GET":
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser] 
    
    def get_permissions(self):
        if self.request.method in {"GET", "PATCH", "DELETE","PUT"}:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]



