from rest_framework.permissions import BasePermission
from rest_framework import permissions



class IsManager(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user 
                    and request.user.is_authenticated 
                    and
                    getattr(request.user, 'role', None) == 'manager')
    
# class IsAdminorManager(BasePermission):

#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_authenticated 
#                     and
#                     (getattr(request.user, 'role', None) == 'manager' or request.user.is_superuser))