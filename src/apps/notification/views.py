from rest_framework import generics,permissions,status,exceptions
from rest_framework.response import Response
from .serializers import NotificationSerializer
from django.conf import settings
from .mongodb import database

import logging
logger = logging.getLogger('error_logger')

class ListNotificationView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = None

    def get(self, request, *args, **kwargs):
        user = self.request.user

        try:
            db = database.connect_db(settings.MONGODB)
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise exceptions.APIException("Something went wrong")
        
        notifications = db.notification.find({"receiver": user.id})

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)