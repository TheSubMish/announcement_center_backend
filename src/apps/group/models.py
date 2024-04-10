from django.db import models
from django.contrib.auth.models import Group
from src.apps.auth.models import User
from src.apps.common.utills import image_validate
import uuid

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
class Group(Group):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(null=False,blank=False)
    image = models.ImageField(default='',validators=[image_validate])
    admin_id = models.CharField(max_length=255,null=False, blank=False)
    category = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=Category.choices,
        default=Category.WEB,
    )
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