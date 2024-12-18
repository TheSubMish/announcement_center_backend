from django.urls import path

from .views import (
    GroupImpressionView,
    AnnouncementImpressionView,
    AnnouncementLikeDislikeView,
)


urls_pattern = [
    path('group/<uuid:pk>/impression/', GroupImpressionView.as_view(), name='group-impression-api'),
    path('announcement/<uuid:pk>/impression/', AnnouncementImpressionView.as_view(), name='announcement-impression-api'),
    path('announcement/<uuid:pk>/like-dislike/', AnnouncementLikeDislikeView.as_view(), name='announcement-like-dislike-api'),
]