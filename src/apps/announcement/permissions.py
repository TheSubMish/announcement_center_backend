from rest_framework.permissions import BasePermission
from rest_framework import exceptions
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
        user_id = request.user.id

        if not group_id:
            raise exceptions.APIException({'error': 'Group ID is required'})

        try:
            group_member = GroupMember.objects.get(group__group_id=group_id, user__id=user_id)
            if group_member.role in [Role.ADMIN, Role.MODERATOR]:
                return True
            else:
                self.message = "You need to be an admin or moderator to create an announcement"
                return False
        except GroupMember.DoesNotExist:
            raise exceptions.APIException({'error': 'User not a member of this group'})
    
class CanUpdateAnnouncement(BasePermission):

    message = "You don't have permission to update announcement"

    def has_object_permission(self, request, view, obj):
        print("has_object_permission called")
        try:
            group_member = GroupMember.objects.get(group=obj.group, user=obj.user)
            if group_member.role==Role.ADMIN or group_member.role==Role.MODERATOR:
                return True
        except GroupMember.DoesNotExist:
            raise exceptions.APIException({'error': 'User not a member of this group'})
        
        return False

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
            group_member = GroupMember.objects.get(group=obj.group, user=obj.user)
            if group_member.role==Role.ADMIN or group_member.role==Role.MODERATOR:
                return True
        except GroupMember.DoesNotExist:
            raise exceptions.APIException({'error': 'User not a member of this group'})
        
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