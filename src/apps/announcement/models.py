from django.db import models
from src.apps.common.models import BaseModel
from src.apps.common.utills import image_validate
from src.apps.auth.models import UserModelMixin,User
from src.apps.group.models import GroupModelMixin

class PaymentMethod(models.TextChoices):
    KHALTI = 'khalti','Khalti'
    ESEWA = 'e-sewa','E-SEWA'
    PAYPAL = 'paypal','Paypal'

class Announcement(BaseModel,UserModelMixin,GroupModelMixin):
    title = models.CharField(max_length=255,null=False, blank=False)
    description = models.TextField(null=False,blank=False)
    image = models.ImageField(default='',validators=[image_validate],upload_to='announcement')
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
    
class AnnouncementComment(BaseModel):
    announcement = models.ForeignKey(Announcement,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length=255,null=False,blank=False)

    def __str__(self):
        return self.user.username