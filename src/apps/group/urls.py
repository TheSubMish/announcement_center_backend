from django.urls import path
from .views import (
    CreateAnnouncementGroupView,
    UpdateAnnouncementGroupView,
    DestroyAnnouncementGroupView,
    ListAnnouncementGroupView,
    RetrieveAnnouncementGroupView,
    ListUserCreatedAnnouncementGroupView,
    JoinAnnouncementGroupView,
    ListUserJoinedAnnouncementGroupView,
    LeaveAnnouncementGroupView,
    GiveRatingView,
    RetrieveRatingView,
    ChangeMemberRoleView,
    ListGroupMemberView,
)

urlpatterns = [
    path('create/',CreateAnnouncementGroupView.as_view(), name='create-announcement-group-api'),
    path('update/<uuid:pk>/',UpdateAnnouncementGroupView.as_view(),name='update-announcement-group-api'),
    path('delete/<uuid:pk>/',DestroyAnnouncementGroupView.as_view(),name='destroy-announcement-group-api'),
    path('list/',ListAnnouncementGroupView.as_view(),name='list-announcement-group-api'),
    path('retrieve/<uuid:pk>/',RetrieveAnnouncementGroupView.as_view(),name='retrieve-announcement-group-api'),
    path('created-by/user/',ListUserCreatedAnnouncementGroupView.as_view(),name='list-user-created-announcement-group-api'),
    path('join/',JoinAnnouncementGroupView.as_view(),name='join-announcement-group-api'),
    path('joined-by/user/',ListUserJoinedAnnouncementGroupView.as_view(),name='list-group-joined-by-user-api'),
    path('<uuid:pk>/leave/',LeaveAnnouncementGroupView.as_view(),name='leave-announcement-group-api'),
    path('give/rating/',GiveRatingView.as_view(),name='give-rating-api'),
    path('<uuid:pk>/retrieve/rating/',RetrieveRatingView.as_view(),name='retrieve-rating-api'),
    path('member/role/change/',ChangeMemberRoleView.as_view(),name='change-member-role-api'),
    path('<uuid:pk>/list/member/',ListGroupMemberView.as_view(),name='list-group-member-api'),
]