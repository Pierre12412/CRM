from rest_framework import permissions


class IsInSalesTeam(permissions.BasePermission):
    message = "You are not in sales team !"

    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.user_type == 3:
            return True
        return False