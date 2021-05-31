from rest_framework.permissions import BasePermission


def check_inputs(request, check_list):
    data = request.data
    for item in check_list:
        if item not in data:
            return False
        if data[item] == '':
            return False
    return True


class IsOwnerCustomer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user.customer:
            return True
        else:
            return False


class IsOwnerCompany(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user.company:
            return True
        else:
            return False


class IsOwnerPermissionCompany(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.company == request.user.company:
            return True
        return False


class IsOwnerPermissionCustomer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.customer == request.user.customer:
            return True
        return False


class IsOwnerOfContactInfoPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.contactInfo.user == request.user:
            return True
        return False


class IsCompanyPermission(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'company'):
            return True
        else:
            return False


class IsCustomerPermission(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'customer'):
            return True
        else:
            return False


class HasCartPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'cart'):
            if request.user.cart == obj:
                return True
        return False
