from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsBoardOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        u = request.user
        if request.method in SAFE_METHODS:
            return obj.owner_id == u.id or obj.members.filter(pk=u.pk).exists()
        return obj.owner_id == request.user.id


class IsBoardOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.owner == request.user or obj.members.filter(id=request.user.id).exists()
        return obj.owner == request.user or obj.members.filter(id=request.user.id).exists()


class IsBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id
    
class IsBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        u = request.user
        if request.method == 'PATCH' or request.method == 'DELETE':
            return obj.members.filter(pk=u.pk).exists()
