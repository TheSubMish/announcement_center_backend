from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import exceptions
from django.contrib.contenttypes.models import ContentType
from src.apps.announcement.models import Announcement
from src.apps.group.models import Group
from django.contrib.auth.models import Permission

@receiver(post_save, sender=User)
def give_user_permission(sender, instance,created,**kwargs):

    if created:
        models_to_grant_permissions = [Announcement,Group]
        for model in models_to_grant_permissions:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            instance.user_permissions.add(*permissions)