from src.apps.common.filters import BaseFilterSet
import django_filters 
from .models import AnnouncementGroup

class AnnouncementGroupFilter(BaseFilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name',lookup_expr='icontains')

    class Meta:
        model = AnnouncementGroup
        fields = ('name','category',)