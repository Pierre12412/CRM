from rest_framework import permissions


class IsInSalesTeam(permissions.BasePermission):
    message = "You are not in sales team !"

    def has_permission(self, request, view):
        try:
            if request.user.user_type == 3 or request.user.user_type == 4:
                return True
        except:
            pass
        return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.user_type == 3 or request.user.user_type == 4:
                return True
        except:
            pass
        return False


class IsInSupportTeam(permissions.BasePermission):
    message = "You are not in support team !"

    def has_permission(self, request, view):
        try:
            if request.user.user_type == 2 or request.user.user_type == 4:
                return True
        except:
            pass
        return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.user_type == 2 or request.user.user_type == 4:
                return True
        except:
            pass
        return False


class IsAdmin(permissions.BasePermission):
    message = "You are not Admin !"

    def has_permission(self, request, view):
        try:
            if request.user.user_type == 4:
                return True
        except:
            pass
        return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.user_type == 4:
                return True
        except:
            pass
        return False

