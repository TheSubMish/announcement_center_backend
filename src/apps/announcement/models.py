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
    image = models.ImageField(null=False,blank=False,validators=[image_validate],upload_to='announcement')
    paid_for_email = models.BooleanField(default=False)
    paid_amount = models.FloatField(default=0.0)
    payment_method = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=PaymentMethod.choices,
        default=PaymentMethod.KHALTI,
    )
    pidx = models.CharField(max_length=255,blank=True,null=True)
    
    def __str__(self):
        return self.title
    
class AnnouncementComment(BaseModel):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=255, null=False, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # Nested comment structure

    def __str__(self):
        if self.user:
            prefix = "  " * self.get_level()  # Indentation based on nesting level
            return f"{prefix}{self.user.username} - {self.comment[:20]}"  # Truncated comment preview
        else:
            prefix = "  " * self.get_level()
            return f"{prefix}Anonymous - {self.comment[:20]}"

    def get_level(self):
        """Calculates the nesting level of the comment (root = 0)"""
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
