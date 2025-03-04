from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        "ws/chat/",
        consumers.OnlineOfflineStatusChangeConsumer.as_asgi(),
        name="chat-consumer",
    ),
]
