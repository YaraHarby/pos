from rest_framework.permissions import BasePermission
from rest_framework import permissions



class IsManager(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user 
                    and request.user.is_authenticated 
                    and
                    getattr(request.user, 'role', None) == 'Manager')

class IsSeller(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user 
                    and request.user.is_authenticated 
                    and
                    getattr(request.user, 'role', None) == 'Seller')    
    
    
class IsSellerOrManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and 
            (getattr(request.user, 'role', None) in ['Seller', 'Manager'])
        )