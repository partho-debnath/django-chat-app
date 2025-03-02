import json

from channels.generic.websocket import (
    WebsocketConsumer,
    AsyncJsonWebsocketConsumer,
)
from asgiref.sync import async_to_sync, sync_to_async

from .models import ExtendUser


class OnlineOfflineStatusChangeConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.set_and_get_online_status(
            username=self.scope["user"].username,
        )
        self.add_active_friends_and_join_groups(
            self.user.get("my_group_name"),
        )
        self.notify_friends_on_status_change()
        self.accept()

    def disconnect(self, close_code):
        self.notify_friends_on_status_change(is_online=False)
        self.remove_active_friends_and_exit_groups(
            group_name=self.user.get("my_group_name"),
        )
        self.set_and_get_online_status(
            username=self.scope["user"].username,
            is_online=False,
        )
        self.close(close_code)

    def set_and_get_online_status(self, username, is_online=True):
        """
        update the 'channel_name' and 'is_online' status based on
        whether the user is online or offline, and return the user.
        """
        users = ExtendUser.objects.filter(
            username=username,
        )
        users.update(
            channel_name=self.channel_name if is_online else None,
            is_online=is_online,
        )
        user = users.values(
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "channel_name",
            "is_online",
            "my_group_name",
        ).first()
        return user

    def get_online_active_friends(self):
        """
        returns the online active friends.
        """
        friends = (
            ExtendUser.objects.prefetch_related(
                "friends",
            )
            .filter(
                friends__person__username=self.user.get("username"),
                friends__friend__is_online=True,
                # friends__friend__channel_name__isnull=False,
            )
            .values("id", "channel_name", "username", "my_group_name")
        )
        return friends

    def add_active_friends_and_join_groups(
        self,
        group_name: str,
    ):
        """
        add online active friends to your group and add
        yourself to all online active friends' groups.
        """
        online_friends = self.get_online_active_friends()

        for online_friend in online_friends:
            async_to_sync(self.channel_layer.group_add)(
                group_name, online_friend.get("channel_name")
            )
            async_to_sync(self.channel_layer.group_add)(
                online_friend.get("my_group_name"), self.channel_name
            )

    def remove_active_friends_and_exit_groups(self, group_name):
        """
        remove online active friends from your group and remove
        yourself from all online active friends' groups.
        """
        online_friends = self.get_online_active_friends()
        for online_friend in online_friends:
            async_to_sync(self.channel_layer.group_discard)(
                group_name, online_friend.get("channel_name")
            )
            async_to_sync(self.channel_layer.group_discard)(
                online_friend.get("my_group_name"), self.channel_name
            )

    def notify_friends_on_status_change(self, is_online=True):
        """notify all friends when a user comes online or goes offline."""
        remarks = "ONLINE" if is_online else "OFFLINE"

        async_to_sync(self.channel_layer.group_send)(
            self.user.get("my_group_name"),
            {
                "type": "notify.friend",
                "message": {
                    **self.user,
                    "is_online": is_online,
                },
                "remarks": remarks,
            },
        )

    def notify_friend(self, event):
        self.send(
            json.dumps(event),
        )


class ChatServerAsyncJsonConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        print("=========", self.user)
        await super().connect()

    async def disconnect(self, code):
        await self.close(code)
