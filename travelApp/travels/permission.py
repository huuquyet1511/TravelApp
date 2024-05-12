from rest_framework import permissions


class OwnerPermission(permissions.IsAuthenticated): #chi nguoi tao moi co quyen thay doi
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user==obj.user