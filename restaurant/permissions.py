from rest_framework.permissions import BasePermission

class IsRestaurantStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'staff'

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'customer'
    
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user