from rest_framework import generics,exceptions,status
from rest_framework.response import Response
from .serializers import (
    CreateAnnouncementSerializer,
    UpdateAnnouncementSerializer,
    AnnouncementSerializer,
    CreateAnnouncementCommentSerializer,
    UpdateAnnouncementCommentSerializer,
    AnnouncementCommentSerializer,
    AnnouncementLikeSerializer,
)
from .permissions import (
    CanCreateAnnouncement,
    CanUpdateAnnouncement,
    CanViewAnnouncement,
    CanDeleteAnnouncement,
    CanUpdateComment,
    CanDeleteComment,
)
from rest_framework.permissions import IsAuthenticated
from .models import Announcement,AnnouncementComment,AnnouncementLike
from src.apps.group.models import AnnouncementGroup
from src.apps.common.models import Status
from src.apps.notification.tasks import announcement_like_unlike_notification
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger('info_logger')

class CreateAnnouncementView(generics.CreateAPIView):
    serializer_class = CreateAnnouncementSerializer
    permission_classes = [CanCreateAnnouncement]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg":"Announcement created successfully"}, status=status.HTTP_201_CREATED)

class UpdateAnnouncementView(generics.UpdateAPIView):
    serializer_class = UpdateAnnouncementSerializer
    permission_classes = [CanUpdateAnnouncement]
    queryset = Announcement.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement = Announcement.objects.select_related("user","group").get(id=id)
        except Announcement.DoesNotExist:
            raise exceptions.NotFound({'error': 'Announcement does not exist'})
        self.check_object_permissions(self.request, announcement)
        return announcement
    

class ListAnnouncementsView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [CanViewAnnouncement]
    queryset = Announcement.objects.all()

    def get_queryset(self):
        group_id = self.kwargs.get('pk', None)
        try:
            announcement_group = AnnouncementGroup.objects.get(group_id=group_id)
        except AnnouncementGroup.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement group does not exist'})
        
        announcements = Announcement.objects.select_related("user","group").filter(group=announcement_group,status="active").order_by('-created_at')
        return announcements
    

class RetrieveAnnouncementView(generics.RetrieveAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [CanViewAnnouncement]
    queryset = Announcement.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement = Announcement.objects.select_related("user","group").get(id=id)
        except Announcement.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement does not exist'})
        return announcement
    

class DeleteAnnouncementView(generics.DestroyAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [CanDeleteAnnouncement]
    queryset = Announcement.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement = Announcement.objects.get(id=id)
        except Announcement.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement does not exist'})
        self.check_object_permissions(self.request, announcement)
        return announcement
    
class CreateAnnouncementCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateAnnouncementCommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ListAnnouncementCommentsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all()

    def get_queryset(self):
        announcement_id = self.kwargs.get('pk', None)
        try:
            announcement = Announcement.objects.get(id=announcement_id)
        except Announcement.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement does not exist'})

        announcement_comments = AnnouncementComment.objects.filter(announcement=announcement, parent__isnull=True).prefetch_related('replies').order_by('-created_at')
        return announcement_comments
    
    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    "id": "uuid",
                    "level": "string",
                    "replies": "string",
                    "status": "string",
                    "created_at": "datetime",
                    "updated_at": "datetime",
                    "announcement": "uuid",
                    "user": "uuid",
                    "parent": "uuid",
                }
            }
        }
    )
    def get(self, request, *args, **kwargs):
        announcement_comments = self.get_queryset()
        filter_queryset = self.filter_queryset(announcement_comments)
        if self.pagination_class:
            page = self.paginate_queryset(filter_queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=announcement_comments,many=True)
       
        return Response(serializer.data,status=status.HTTP_200_OK)

class RetrieveAnnouncementCommentsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement_comment = AnnouncementComment.objects.get(id=id,status=Status.ACTIVE)
        except AnnouncementComment.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement comment does not exist'})
        return announcement_comment
    
    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    "id": "uuid",
                    "level": "string",
                    "replies": "string",
                    "status": "string",
                    "created_at": "datetime",
                    "updated_at": "datetime",
                    "announcement": "uuid",
                    "user": "uuid",
                    "parent": "uuid",
                }
            }
        }
    )
    def get(self,request, *args, **kwargs):
        announcement_comment = self.get_object()
        serializer = self.get_serializer(instance=announcement_comment)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UpdateAnnouncementCommentView(generics.UpdateAPIView):
    permission_classes = [CanUpdateComment]
    serializer_class = UpdateAnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement_comment = AnnouncementComment.objects.get(id=id)
        except AnnouncementComment.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement comment does not exist'})
        self.check_object_permissions(self.request, announcement_comment)
        return announcement_comment
    

class DeleteAnnouncementCommentView(generics.DestroyAPIView):
    permission_classes = [CanDeleteComment]
    serializer_class = AnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement_comment = AnnouncementComment.objects.get(id=id)
        except AnnouncementComment.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement comment does not exist'})
        self.check_object_permissions(self.request, announcement_comment)
        return announcement_comment
    

class AnnouncementLikeView(generics.GenericAPIView):
    serializer_class = AnnouncementLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            announcement = Announcement.objects.get(id=announcement_id)
        except Announcement.DoesNotExist:
            return Response({'error': 'Announcement does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        user_like = AnnouncementLike.objects.update_or_create(
            user=user, 
            announcement=announcement,
            defaults={
                'like': serializer.validated_data.get("like",False),
                'dislike': serializer.validated_data.get("dislike",False)
            }
        )

        if user_like.like:
            announcement_like_unlike_notification.delay(user_like.id, "like")
        if user_like.dislike:
            announcement_like_unlike_notification.delay(user_like.id, "dislike")

        return Response({"msg":"Updated successfully"})
