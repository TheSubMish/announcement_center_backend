from django.urls import path
from .views import ListNotificationView

urlpatterns = [
    path('list/', ListNotificationView.as_view(), name='list-notification-api'),
]