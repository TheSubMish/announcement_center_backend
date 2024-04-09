from django.db import models
from django.contrib.auth.models import Group
from src.apps.auth.models import User
from src.apps.common.utills import image_validate
import uuid

# Create your models here.
class Group(Group):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(null=False,blank=False)
    image = models.ImageField(default='',validators=[image_validate])
    admin_id = models.CharField(max_length=255,null=False, blank=False)
    members = models.ManyToManyField(User)
    total_members = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class GroupModelMixin(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)

    class Meta:
        abstract = True