from django.urls import path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path("ws/v1/notification/<str:user_id>/", NotificationConsumer.as_asgi()),
]