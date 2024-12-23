from django.urls import path

from .views import (
    GroupImpressionView,
    GroupImpressionCountryCityView,
    GroupRateAnalyticsView,
    AnnouncementImpressionView,
    AnnouncementLikeDislikeView,
)


urlpatterns = [
    path('group/<uuid:pk>/impression/', GroupImpressionView.as_view(), name='group-impression-api'),
    path('group/<uuid:pk>/impression/country-city/', GroupImpressionCountryCityView.as_view(), name='group-impression-country-city-api'),
    path('group/<uuid:pk>/rate/', GroupRateAnalyticsView.as_view(), name='group-rate-api'),
    path('announcement/<uuid:pk>/impression/', AnnouncementImpressionView.as_view(), name='announcement-impression-api'),
    path('announcement/<uuid:pk>/like-dislike/', AnnouncementLikeDislikeView.as_view(), name='announcement-like-dislike-api'),
]
