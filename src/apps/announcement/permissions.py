from rest_framework.permissions import BasePermission

class CanCreateAnnouncement(BasePermission):

    message = "You don't have permission to create announcement"

    def has_object_permission(self, request, view, obj):
        if obj.group.admin_id == request.user.id:
            return True
        return False

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('announcement.add_announcement')
        )
    
class CanUpdateAnnouncement(BasePermission):

    message = "You don't have permission to update announcement"

    def has_object_permission(self, request, view, obj):
        if obj.admin == request.user:
            return True
        return False

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('announcement.add_announcement')
        )
    
class CanViewAnnouncement(BasePermission):

    message = "You don't have permission to view announcement"

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('announcement.view_announcement')
        )
    
class CanDeleteAnnouncement(BasePermission):

    message = "You don't have permission to delete announcement"

    def has_object_permission(self, request, view, obj):
        if obj.admin == request.user:
            return True
        return False
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('announcement.delete_announcement')
        )
    

class CanUpdateComment(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('announcement.update_announcement_comment')
        )
    
class CanDeleteComment(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('announcement.delete_announcement_comment')
        )