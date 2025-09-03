# from rest_framework.permissions import BasePermission

# class IsManger (BasePermission):
#     def has_permission(self, request, view):
#         if not request.user or not request.user.is_authenticated:
#             return False
#         role_name = getattr (request.user.type, "name","").lower()
#         return role_name == "manager" 

    