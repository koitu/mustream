from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    only allow owner to access/edit
    Assumes that model instance has an 'owner' attribute
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    

class IsOwnerOrIsPublic(permissions.BasePermission):
    """
    only allow owner to access/edit
    Assumes that model instance has an 'owner' attribute
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.public
        return obj.owner == request.user
