from django.db import models

from src.apps.common.models import BaseModel
from src.apps.group.models import AnnouncementGroup

class GroupPayment(BaseModel):
    group = models.ForeignKey(AnnouncementGroup, on_delete=models.SET_NULL, null=True, blank=True)