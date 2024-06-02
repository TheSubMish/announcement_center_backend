from django.db import models
from django.contrib.auth.models import Group
from src.apps.auth.models import User
from src.apps.common.utills import image_validate
import uuid
from src.apps.common.models import BaseModel
from django.db.models import Avg

class Category(models.TextChoices):
    WEB = 'web','Web'
    NETWORK = 'network','Network'
    CYBER = 'cyber','Cyber'
    CLOUD = 'cloud','Cloud'
    ART = 'art','Art'
    FOOD = 'food','Food'
    ENTERTAINMENT = 'entertainment','Entertainment'
    HEALTH = 'health','Health'
    LIFESTYLE = 'lifestyle','Lifestyle'
    SPORTS ='sports','Sports'
    TRAVEL = 'travel','Travel'
    OTHER = 'other','Other'

# Create your models here.
class AnnouncementGroup(Group):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(null=False,blank=False)
    image = models.ImageField(default='',validators=[image_validate])
    admin = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    category = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=Category.choices,
        default=Category.WEB,
    )
    total_members = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def average_rating(self) -> float:
        return Rating.objects.filter(group=self).aggregate(Avg("rating"))["rating__avg"]

    def __str__(self):
        return self.name
    
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