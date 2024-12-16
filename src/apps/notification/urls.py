from django.urls import path
# from .views import ListNotificationView,ReadNotificationView
from .views import ListNotificationView, UpdateNotificationView

urlpatterns = [
    path('list/', ListNotificationView.as_view(), name='list-notification-api-endpoint'),
    path('<uuid:pk>/update/', UpdateNotificationView.as_view(), name='read-notification-api-endpoint'),
]