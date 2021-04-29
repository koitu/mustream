from rest_framework import permissions

class TrackPermission(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.force_private:
                return False
            return (obj.album and obj.album.public) or (obj.artist and obj.artist.public) or obj.public
        return obj.owner == request.user


class OtherPermission(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.public
        else:
            return obj.owner == request.user

