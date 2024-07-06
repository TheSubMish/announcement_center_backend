from django.db import models
from django.contrib.auth.models import Group
from src.apps.auth.models import User
from src.apps.common.utills import image_validate
import uuid
from src.apps.common.models import BaseModel,Status
from django.db.models import Avg
from django_ckeditor_5.fields import CKEditor5Field

class Category(BaseModel):
    name = models.CharField(max_length=255,null=False,blank=False)
    created_by = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL)

    def delete(self, *args, **kwargs):
        self.status = Status.INACTIVE
        self.save()

    def __str__(self) -> str:
        return self.name

class GroupType(models.TextChoices):
    PUBLIC = 'public','Public'
    PRIVATE = 'private','Private'

# Create your models here.
class AnnouncementGroup(Group):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = CKEditor5Field('Description',config_name='extends')
    image = models.ImageField(default='',validators=[image_validate],upload_to='groups/')
    admin = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.SET_NULL)
    group_type = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=GroupType.choices,
        default=GroupType.PUBLIC
    )
    total_members = models.IntegerField(default=1)
    location = models.CharField(max_length=255,null=True,blank=True)

    invite_code = models.CharField(max_length=255,null=True,blank=True)
    code_expires_at = models.DateTimeField(null=True, blank=True)

    premium_group = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def average_rating(self) -> float:
        return Rating.objects.filter(group=self).aggregate(Avg("rating"))["rating__avg"]

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.status = Status.INACTIVE
        self.save()
    
class GroupModelMixin(models.Model):
    group = models.ForeignKey(AnnouncementGroup,on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Rating(BaseModel):
    group = models.ForeignKey(AnnouncementGroup,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.username
    
    def delete(self, *args, **kwargs):
        self.status = Status.INACTIVE
        self.save()
    
class Role(models.TextChoices):
    MEMBER = 'member','Member'
    MODERATOR = 'moderator','Moderator'
    ADMIN = 'admin','Admin'
    
class GroupMember(BaseModel):
    group = models.ForeignKey(AnnouncementGroup,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.CharField(
        max_length=255,
        null= False,
        blank=False,
        choices=Role.choices,
        default=Role.MEMBER,
    )

    def delete(self, *args, **kwargs):
        self.status = Status.INACTIVE
        self.save()