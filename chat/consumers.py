import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import ExtendUser, Friends


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self):
        # _ = ExtendUser.objects.filter(
        #     username=self.scope["user"].username,
        # ).update(
        #     channel_name=self.channel_name,
        #     is_online=True,
        # )
        self.user_connected()
        self.accept()

    def disconnect(self, close_code):
        user = ExtendUser.objects.filter(
            username=self.scope["user"].username,
        ).update(
            channel_name=None,
            is_online=False,
        )
        self.close(close_code)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json.get("type") == "online_friends":
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    "type": "online.friends",
                    "message": "online fiends",
                },
            )

    # def chat_message(self, event):
    #     self.send(json.dumps(event))

    def user_connected(self):
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
        for friend in friends:
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    "type": "notify.friend",
                    "message": friend,
                },
            )

    def notify_friend(self, event):
        self.send(
            json.dumps(event),
        )

    def online_friends(self, event):
        online_active_friends = (
            Friends.objects.filter(
                person__username=self.scope["user"].username,
                friend__is_online=True,
            )
            .select_related("friend")
            .values(
                "id",
                "friend__username",
                "friend__channel_name",
                "friend__first_name",
                "friend__last_name",
            )
        )

        # print("online_active_friends", online_active_friends)
        self.send(
            json.dumps(
                {
                    "friends": list(online_active_friends),
                    "message": event.get("message"),
                },
            ),
        )
