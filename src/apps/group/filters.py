from src.apps.common.filters import BaseFilterSet
import django_filters 
from .models import AnnouncementGroup

class AnnouncementGroupFilter(BaseFilterSet):
    category = django_filters.CharFilter(field_name='category',lookup_expr='iexact')

    class Meta:
        model = AnnouncementGroup
        fields = ('category',)