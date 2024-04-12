from django.urls import path
from .views import (
    CreateAnnouncementGroupView,
    UpdateAnnouncementGroupView,
    DestroyAnnouncementGroupView,
    ListAnnouncementGroupView,
    ListUserCreatedAnnouncementGroupView,
    JoinAnnouncementGroupView
)

urlpatterns = [
    path('create/',CreateAnnouncementGroupView.as_view(), name='create-announcement-group-api'),
    path('update/<uuid:pk>/',UpdateAnnouncementGroupView.as_view(),name='update-announcement-group-api'),
    path('delete/<uuid:pk>/',DestroyAnnouncementGroupView.as_view(),name='destroy-announcement-group-api'),
    path('list/',ListAnnouncementGroupView.as_view(),name='list-announcement-group-api'),
    path('list/created/',ListUserCreatedAnnouncementGroupView.as_view(),name='list-user-created-announcement-group'),
    path('join/',JoinAnnouncementGroupView.as_view(),name='join-announcement-group-api'),
]