from rest_framework import generics,exceptions,status
from rest_framework.response import Response
from .serializers import (
    CreateAnnouncementSerializer,
    UpdateAnnouncementSerializer,
    AnnouncementSerializer,
    CreateAnnouncementCommentSerializer,
    UpdateAnnouncementCommentSerializer,
    AnnouncementCommentSerializer,
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
from .models import Announcement,AnnouncementComment
from src.apps.group.models import AnnouncementGroup
import logging

logger = logging.getLogger('info_logger')

class CreateAnnouncementView(generics.CreateAPIView):
    serializer_class = CreateAnnouncementSerializer
    permission_classes = [CanCreateAnnouncement]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateAnnouncementView(generics.UpdateAPIView):
    serializer_class = UpdateAnnouncementSerializer
    permission_classes = [CanUpdateAnnouncement]
    queryset = Announcement.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement = Announcement.objects.get(id=id)
        except Announcement.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement does not exist'})
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
        
        announcements = Announcement.objects.filter(group=announcement_group).order_by('-created_at')
        return announcements
    

class RetrieveAnnouncementView(generics.RetrieveAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [CanViewAnnouncement]
    queryset = Announcement.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement = Announcement.objects.get(id=id)
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
        logger.info(f'Announcement: {announcement.title} deleting by user: {self.request.user.username}')
        return announcement
    
class CreateAnnouncementCommentView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CreateAnnouncementCommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ListAnnouncementCommentsView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
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
    

class RetrieveAnnouncementCommentsView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement_comment = AnnouncementComment.objects.get(id=id)
        except AnnouncementComment.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement comment does not exist'})
        return announcement_comment

class UpdateAnnouncementCommentView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated,CanUpdateComment]
    serializer_class = UpdateAnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement_comment = AnnouncementComment.objects.get(id=id)
        except AnnouncementComment.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement comment does not exist'})
        return announcement_comment
    

class DeleteAnnouncementCommentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,CanDeleteComment]
    serializer_class = AnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement_comment = AnnouncementComment.objects.get(id=id)
        except AnnouncementComment.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement comment does not exist'})
        logger.info(f'Anouncement comment {announcement_comment} deleting by user {self.request.user.username}')
        return announcement_comment