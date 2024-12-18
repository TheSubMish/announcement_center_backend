from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta

from src.apps.group.models import AnnouncementGroup, GroupMember
from src.apps.announcement.models import Announcement, AnnouncementLike, AnnouncementComment

from .serializers import ImpressionSerializer,AnnouncementLikeDislikeSerializer
from .models import GroupImpression, AnnouncementImpression


class GroupImpressionView(APIView):

    def get(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')

        try:
            group = AnnouncementGroup.objects.get(pk=group_id)
            if not group.premium_group:
                return Response({'error': 'You do not have permission'}, status=403)
            
            if not GroupMember.objects.filter(
                group=group,
                user=request.user,
                role__in=["admin", "moderator"]
            ).exists():
                return Response({'error': 'You do not have permission'}, status=403)
            
        except AnnouncementGroup.DoesNotExist:
            return Response({'error': 'Announcement group does not exist'}, status=404)

        today = timezone.now().date()

        # Calculate the date 7 days ago
        last_week = today - timedelta(days=7)

        # Query to count impressions per day
        impressions_per_day = (
            GroupImpression.objects
            .filter(group=group,created_at__date__gte=last_week, created_at__date__lte=today)
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        serializer = ImpressionSerializer(impressions_per_day,many=True)
        
        return Response(serializer.data)
    

class AnnouncementImpressionView(generics.GenericAPIView):
    serializer_class = ImpressionSerializer

    def get(self, request, *args, **kwargs):
        announcement_id = kwargs.get('pk')

        try:
            announcement = Announcement.objects.get(pk=announcement_id)
            if not announcement.group.premium_group:
                return Response({'error': 'You do not have permission'}, status=403)
            
            if not GroupMember.objects.filter(
                group=announcement.group,
                user=request.user,
                role__in=["admin", "moderator"]
            ).exists():
                return Response({'error': 'You do not have permission'}, status=403)
            
        except AnnouncementGroup.DoesNotExist:
            return Response({'error': 'Announcement group does not exist'}, status=404)

        today = timezone.now().date()

        # Calculate the date 7 days ago
        last_week = today - timedelta(days=7)

        # Query to count impressions per day
        impressions_per_day = (
            AnnouncementImpression.objects
            .filter(announcement=announcement,created_at__date__gte=last_week, created_at__date__lte=today)
            .annotate(day=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        serializer = ImpressionSerializer(impressions_per_day,many=True)
        
        return Response(serializer.data)
    


class AnnouncementLikeDislikeView(APIView):

    def get(self,request, *args, **kwargs):
        announcement_id = kwargs.get('pk')

        try:
            announcement = Announcement.objects.get(pk=announcement_id)
            if not announcement.group.premium_group:
                return Response({'error': 'You do not have permission'}, status=403)
            
            if not GroupMember.objects.filter(
                group=announcement.group,
                user=request.user,
                role__in=["admin", "moderator"]
            ).exists():
                return Response({'error': 'You do not have permission'}, status=403)
            
        except AnnouncementGroup.DoesNotExist:
            return Response({'error': 'Announcement group does not exist'}, status=404)
        
        today = timezone.now().date()

        # Calculate the date 7 days ago
        last_week = today - timedelta(days=7)

        likes = (
            AnnouncementLike.objects.filter(
                announcement=announcement,
                created_at__date__gte=last_week, 
                created_at__date__lte=today,
                like=True
            )
            .annotate(day=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        like_serializer = AnnouncementLikeDislikeSerializer(likes)

        dislikes = (
            AnnouncementLike.objects.filter(
                announcement=announcement,
                created_at__date__gte=last_week, 
                created_at__date__lte=today,
                like=True
            )
            .annotate(day=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        dislike_serializer = AnnouncementLikeDislikeSerializer(dislikes)

        data = {
            "likes": like_serializer.data,
            "dislikes": dislike_serializer.data,
        }

        return Response(data)
