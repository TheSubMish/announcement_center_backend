from django.db import models
from src.apps.common.models import BaseModel
from src.apps.common.utills import image_validate
from src.apps.auth.models import UserModelMixin
from src.apps.group.models import GroupModelMixin

class PaymentMethod(models.TextChoices):
    KHALTI = 'khalti','Khalti'
    ESEWA = 'e-sewa','E-SEWA'
    PAYPAL = 'paypal','Paypal'

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


class Announcement(BaseModel,UserModelMixin,GroupModelMixin):
    title = models.CharField(max_length=255,null=False, blank=False)
    description = models.TextField(null=False,blank=False)
    image = models.ImageField(default='',validators=[image_validate],upload_to='announcement')
    category = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=Category.choices,
        default=Category.WEB,
    )
    paid_for_email = models.BooleanField(default=True)
    paid_amount = models.IntegerField(default=0)
    payment_method = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=PaymentMethod.choices,
        default=PaymentMethod.KHALTI,
    )

    def __str__(self):
        return self.title