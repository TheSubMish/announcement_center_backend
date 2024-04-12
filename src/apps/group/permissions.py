from rest_framework.permissions import BasePermission

class CanCreateAnnouncementGroup(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('group.add_announcementgroup')
        )
    

class CanUpdateAnnouncementGroup(BasePermission):

    message = "You cannot update this announcement group"
    
    def has_object_permission(self, request, view, obj):
        if obj.admin_id == request.user.id:
            return True
        return False
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('group.change_announcementgroup')
        )
    

class CanDeleteAnnouncementGroup(BasePermission):
    message = "You cannot delete this announcement group"

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('group.delete_announcementgroup')
        )
    
    def has_object_permission(self, request, view, obj):
        if obj.admin_id == request.user.id:
            return True
        return False

class CanViewAnnouncementGroup(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('group.view_announcementgroup')
        )