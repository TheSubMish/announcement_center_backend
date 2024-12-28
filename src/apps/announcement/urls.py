from django.urls import path
from .views import (
    CreateAnnouncementView,
    UpdateAnnouncementView,
    ListAnnouncementsView,
    RetrieveAnnouncementView,
    DeleteAnnouncementView,
    CreateAnnouncementCommentView,
    UpdateAnnouncementCommentView,
    ListAnnouncementCommentsView,
    RetrieveAnnouncementCommentsView,
    DeleteAnnouncementCommentView,
    AnnouncementLikeView,
    AnnouncementInterestedView,
)


urlpatterns = [
    path('create/', CreateAnnouncementView.as_view(), name='create-announcement-api'),
    path('update/<uuid:pk>/', UpdateAnnouncementView.as_view(), name='update-announcement-api'),
    path('list/group/<uuid:pk>/', ListAnnouncementsView.as_view(), name='list-announcements-api'),
    path('retrieve/<uuid:pk>/', RetrieveAnnouncementView.as_view(), name='retrieve-announcement-api'),
    path('delete/<uuid:pk>/', DeleteAnnouncementView.as_view(), name='delete-announcement-api'),
    path('give/comment/',CreateAnnouncementCommentView.as_view(),name='give-announcement-comment-api'),
    path('comment/update/<uuid:pk>/', UpdateAnnouncementCommentView.as_view(), name='update-announcement-comment-api'),
    path('<uuid:pk>/comment/list/', ListAnnouncementCommentsView.as_view(), name='list-announcement-comments-api'),
    path('comment/retrieve/<uuid:pk>/', RetrieveAnnouncementCommentsView.as_view(), name='retrieve-announcement-comments-api'),
    path('comment/delete/<uuid:pk>/', DeleteAnnouncementCommentView.as_view(), name='delete-announcement-comment-api'),
    path('like/', AnnouncementLikeView.as_view(), name='like-announcement-api'),
    path('interested/', AnnouncementInterestedView.as_view(), name='interested-announcement-api'),
]