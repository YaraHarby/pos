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
    


class TenantModulePermission(BasePermission):
    """
    يسمح بالوصول إذا:
    - المستخدم Manager أو Seller (دائمًا مسموح)
    - المستخدم Kitchen أو Delivery و الموديل مفعل في tenant.modules_enabled
    """

    role_module_map = {
        "kitchen": "kitchen",
        "Delivery": "Delivery",
        # Manager و Seller غير موجودين هنا لأنهم مسموح لهم دائمًا
    }

    def has_permission(self, request, view):
        user = request.user
        tenant = getattr(request, "tenant", None)  # middleware من django-tenants

        if not tenant:
            return False  # لو مفيش tenant، ممنوع الوصول

        # Manager و Seller مسموح لهم دائمًا
        if user.role in ["Manager", "Seller"]:
            return True

        # باقي الـ roles تتحقق من modules_enabled
        module_key = self.role_module_map.get(user.role)
        if module_key is None:
            return False  # role غير معروف، ممنوع

        return tenant.modules_enabled.get(module_key, False)