import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import ExtendUser, Friends


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        _ = ExtendUser.objects.filter(
            username=self.scope["user"].username,
        ).update(
            channel_name=self.channel_name,
            is_online=True,
        )
        self.user_online_status_updated()
        self.accept()

    def disconnect(self, close_code):
        self.user_online_status_updated(is_online=False)
        _ = ExtendUser.objects.filter(
            username=self.scope["user"].username,
        ).update(
            channel_name=None,
            is_online=False,
        )
        self.close(close_code)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                "type": "online.friends",
                "message": "online fiends",
            },
        )

    def chat_message(self, event):
        self.send(json.dumps(event))

    def user_online_status_updated(self, is_online=True):
        """notify all friends when someone is on online or offline."""
        friends = (
            ExtendUser.objects.prefetch_related(
                "friends",
            )
            .filter(
                friends__person__username=self.scope["user"].username,
                friends__friend__is_online=True,
                # friends__friend__channel_name__isnull=False,
            )
            .values("id", "channel_name", "username")
        )
        remarks = "new friend online" if is_online else "friend offline."
        for friend in friends:
            async_to_sync(self.channel_layer.send)(
                friend.get("channel_name"),
                {
                    "type": "notify.friend",
                    "message": friend,
                    "remarks": remarks,
                },
            )

    def notify_friend(self, event):
        self.send(
            json.dumps(event),
        )
