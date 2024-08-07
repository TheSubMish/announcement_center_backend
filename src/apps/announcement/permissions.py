from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from src.apps.group.models import GroupMember,Role

class CanCreateAnnouncement(BasePermission):

    message = "You don't have permission to create announcement"

    def has_permission(self, request, view):
        if ( not request.user or
            not request.user.is_authenticated or 
            not request.user.has_perm('announcement.add_announcement')
        ):
            return False

        group_id = request.data.get('group')

        if not group_id:
            raise PermissionDenied({'error': 'Group ID is required'})

        try:
            group_member = GroupMember.objects.get(group__group_id=group_id, user=request.user)
            if group_member.role==Role.MEMBER:
                return False
            else:
                return True
        except GroupMember.DoesNotExist:
            raise PermissionDenied({'error': 'User is not a member of this group'})
    
class CanUpdateAnnouncement(BasePermission):

    message = "You don't have permission to update announcement"

    def has_object_permission(self, request, view, obj):
        try:
            group_member = GroupMember.objects.get(group=obj.group, user=request.user)
            if group_member.role==Role.MEMBER:
                return False
        except GroupMember.DoesNotExist:
            raise PermissionDenied({'error': 'User is not a member of this group'})
        
        return True

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('announcement.change_announcement')
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
        try:
            group_member = GroupMember.objects.get(group=obj.group, user=request.user)
            if group_member.role==Role.ADMIN:
                return True
        except GroupMember.DoesNotExist:
            raise PermissionDenied({'error': 'User is not a member of this group'})
        
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
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
        print(f"Has change_announcement_comment permission: {request.user.has_perm('announcement_comment.change_announcement_comment')}")
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.has_perm('announcement.change_announcementcomment')
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
            request.user.has_perm('announcement.delete_announcementcomment')
        )