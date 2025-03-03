from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        "ws/chat/",
        consumers.OnlineOfflineStatusChangeConsumer.as_asgi(),
        name="chat-consumer",
    ),
    re_path(
        "ws/chat-server/",
        consumers.ChatServerAsyncJsonConsumer.as_asgi(),
        name="chat-server",
    ),
]
