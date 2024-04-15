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
    CanDeleteAnnouncement
)
from .models import Announcement,AnnouncementComment
from src.apps.group.models import AnnouncementGroup

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
        

        announcements = Announcement.objects.filter(group=announcement_group)
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
        return announcement
    
class CreateAnnouncementCommentView(generics.CreateAPIView):

    serializer_class = CreateAnnouncementCommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class UpdateAnnouncementCommentView(generics.UpdateAPIView):
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
    serializer_class = AnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement_comment = AnnouncementComment.objects.get(id=id)
        except AnnouncementComment.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement comment does not exist'})
        return announcement_comment
    

class ListAnnouncementCommentsView(generics.ListAPIView):

    serializer_class = AnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all()

    def get_queryset(self):
        announcement_id = self.kwargs.get('pk', None)
        try:
            announcement = Announcement.objects.get(id=announcement_id)
        except Announcement.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement does not exist'})

        announcement_comments = AnnouncementComment.objects.filter(announcement=announcement)
        return announcement_comments
    

class RetrieveAnnouncementCommentsView(generics.RetrieveAPIView):

    serializer_class = AnnouncementCommentSerializer
    queryset = AnnouncementComment.objects.all()

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            announcement_comment = AnnouncementComment.objects.get(id=id)
        except AnnouncementComment.DoesNotExist:
            raise exceptions.APIException({'error': 'Announcement comment does not exist'})
        return announcement_comment