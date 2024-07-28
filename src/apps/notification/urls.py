from django.urls import path
from .views import ListNotificationView,ReadNotificationView

urlpatterns = [
    path('list/', ListNotificationView.as_view(), name='list-notification-api-endpoint'),
    path('read/', ReadNotificationView.as_view(), name='read-notification-api-endpoint'),
]