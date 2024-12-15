from rest_framework import generics,permissions,status,exceptions
from rest_framework.response import Response
# from .serializers import NotificationSerializer,ReadNotificationSerializer
from .serializers import NotificationSerializer, NotificationReadSerializer
from .models import Notification
from django.conf import settings
from .mongodb import database
from pymongo import DESCENDING
from uuid import UUID

import logging
logger = logging.getLogger('error_logger')


class ListNotificationView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationReadSerializer
    queryset = None

    def get_queryset(self):
        user = self.request.user

        notifications = Notification.objects.filter(receiver=user)

        return notifications
    

class UpdateNotificationView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = None

    def get_object(self):
        notification_id = self.kwargs.get('pk', None)

        try:
            notification = Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            raise exceptions.APIException({'error': 'Notification does not exist'})

        if notification.receiver!= self.request.user:
            raise exceptions.PermissionDenied()

        return notification


# class ListNotificationView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = NotificationSerializer
#     queryset = None

#     def get(self, request, *args, **kwargs):
#         user = self.request.user

#         try:
#             db = database.connect_db(settings.MONGODB)
#         except Exception as e:
#             logger.error(f"Failed to connect to MongoDB: {e}")
#             raise exceptions.APIException("Something went wrong")
        
#         notifications = db.notification.find({"receiver": user.id}).sort("created_at", DESCENDING)

#         serializer = NotificationSerializer(notifications, many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
# class ReadNotificationView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = ReadNotificationSerializer

#     def patch(self, request, *args, **kwargs):
#         notification_id = request.data.get('notification_id')
#         read = request.data.get('read')

#         try:
#             db = database.connect_db(settings.MONGODB)
#         except Exception as e:
#             logger.error(f"Failed to connect to MongoDB: {e}")
#             raise exceptions.APIException("Something went wrong")
        
#         notification = db.notification.find_one_and_update(
#             {"_id": UUID(notification_id)},
#             {"$set": {"read": read}},
#             return_document=True
#         )

#         if notification is None:
#             raise exceptions.APIException('Notification not found')

#         serializer = NotificationSerializer(notification)
#         return Response(serializer.data, status=status.HTTP_200_OK)