from django.db import models

from src.apps.common.models import BaseModel
from src.apps.group.models import AnnouncementGroup
from src.apps.auth.models import User


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'
    EXPIRED = 'expired', 'Expired'
    REFUNDED = 'refunded', 'Refunded'

class GroupPayment(BaseModel):
    group = models.ForeignKey(AnnouncementGroup, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_intent = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    recurring_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(
        max_length=255, 
        null=True, blank=True, 
        default=PaymentStatus.PENDING,
        choices=PaymentStatus.choices
    )

    def __str__(self):
        return f"Payment for Group {self.group.name if self.group else "unknown"} by {self.user.username if self.user else "unknown"}"