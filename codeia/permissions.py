from enum import Enum
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class Role(Enum):
    GUEST = 'guest'
    PHOTOGRAPHER = 'photographer'
    SUPERSTAR = 'superstar'
    AMBASSADOR = 'ambassador'
    ADMIN = 'admin'

class IsGuestUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous

class IsAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied(detail="User not authenticated")
        elif user.role != Role.ADMIN.value:
            raise PermissionDenied(detail="User is not admin")
        return True
    
class IsPhotographerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied(detail="User not authenticated")
        elif user.role != Role.PHOTOGRAPHER.value:
            raise PermissionDenied(detail="User is not photographer")
        return True
    
class IsAmbassadorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied(detail="User not authenticated")
        elif user.role != Role.AMBASSADOR.value:
            raise PermissionDenied(detail="User is not ambassador")
        return True