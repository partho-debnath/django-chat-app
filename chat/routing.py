from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<room_name>\w+)/$",
        consumers.OnlineOfflineStatusChangeConsumer.as_asgi(),
        name="chat-consumer",
    ),
    re_path(
        "ws/chat-server/",
        consumers.ChatServerAsyncJsonConsumer.as_asgi(),
        name="chat-server",
    ),
]
