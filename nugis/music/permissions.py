from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsUploaderOrReadOnly(BasePermission):
    """Anyone logged in can listen; only the uploader (or staff) can edit/delete."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or obj.upload_by_id == request.user.id


class IsStaffOrReadOnly(BasePermission):
    """Catalog (albums, artists, genres) is editable by staff only."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff
