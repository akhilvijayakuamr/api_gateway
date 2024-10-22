from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()), #-> websocket chat path
    path('ws/notification/', consumers.NotificationConsumer.as_asgi()), #-> websocket chat path
]