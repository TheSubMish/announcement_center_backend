from rest_framework import generics,permissions, status
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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')

        try:
            group = AnnouncementGroup.objects.get(pk=group_id)
            if not group.premium_group:
                return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
            
            if not GroupMember.objects.filter(
                group=group,
                user=request.user,
                role__in=["admin", "moderator"]
            ).exists():
                return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
            
        except AnnouncementGroup.DoesNotExist:
            return Response({'error': 'Announcement group does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        range = self.request.query_params.get("range", None) # type: ignore
        if range is None:
            return Response({'error': 'range is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        today = timezone.now()
        
        if range == "this_week":
            # Calculate the date 7 days ago
            last_date = today - timedelta(days=7)

        if range == "this_month":
            # Calculate the date 30 days ago
            last_date = today - timedelta(days=30)

        if range == "3_months":
            # Calculate the date 90 days ago
            last_date = today - timedelta(days=90)

        if range == "all_time":
            # Calculate the date 0 days ago
            last_date = timezone.datetime(1970, 1, 1)

        # Query to count impressions per day
        impressions_per_day = (
            GroupImpression.objects
            .filter(group=group,created_at__gte=last_date, created_at__lte=today)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
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

        range = self.request.query_params.get("range", None) # type: ignore
        if range is None:
            return Response({'error': 'range is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        today = timezone.now()
        
        if range == "this_week":
            # Calculate the date 7 days ago
            last_date = today - timedelta(days=7)

        if range == "this_month":
            # Calculate the date 30 days ago
            last_date = today - timedelta(days=30)

        if range == "3 months":
            # Calculate the date 90 days ago
            last_date = today - timedelta(days=90)

        if range == "all_time":
            # Calculate the date 0 days ago
            last_date = timezone.datetime(1970, 1, 1)

        # Query to count impressions per day
        impressions_per_day = (
            AnnouncementImpression.objects
            .filter(announcement=announcement,created_at__gte=last_date, created_at__lte=today)
            .annotate(date=TruncDate('created_at'))
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
        
        range = self.request.query_params.get("range", None) # type: ignore
        if range is None:
            return Response({'error': 'range is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        today = timezone.now()
        
        if range == "this_week":
            # Calculate the date 7 days ago
            last_date = today - timedelta(days=7)

        if range == "this_month":
            # Calculate the date 30 days ago
            last_date = today - timedelta(days=30)

        if range == "3 months":
            # Calculate the date 90 days ago
            last_date = today - timedelta(days=90)

        if range == "all_time":
            # Calculate the date 0 days ago
            last_date = timezone.datetime(1970, 1, 1)

        likes = (
            AnnouncementLike.objects.filter(
                announcement=announcement,
                created_at__gte=last_date, 
                created_at__lte=today,
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
                created_at__gte=last_date, 
                created_at__lte=today,
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
