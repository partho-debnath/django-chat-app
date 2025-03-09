from django.db.models import F, Q
from rest_framework.generics import ListAPIView
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication,
)

from rest_framework.permissions import IsAuthenticated

from chat.models import ExtendUser, Messages


from .serializers import (
    ExtendUserModelSerializer,
    MessagesModelSerializer,
)


class OnlineActiveFriendList(ListAPIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ExtendUserModelSerializer

    queryset = (
        ExtendUser.objects.filter(
            is_online=True,
        )
        .prefetch_related(
            "friends__group",
        )
        .annotate(
            pear_to_pear_group=F("friends__group__name"),
        )
        .only(
            "id",
            "username",
            "channel_name",
            "image",
        )
    )

    def get_queryset(self):
        query_set = (
            super()
            .get_queryset()
            .filter(
                friends__person__username=self.request.user.username,
            )
        )
        return query_set


class OldMessageList(ListAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    serializer_class = MessagesModelSerializer

    queryset = Messages.objects.prefetch_related("files").all()

    def get_queryset(self):
        query_set = (
            super()
            .get_queryset()
            .filter(
                Q(
                    sender_id=self.request.user.id,
                    receiver_id=self.kwargs.get("receiver_id"),
                )
                | Q(
                    sender_id=self.kwargs.get("receiver_id"),
                    receiver_id=self.request.user.id,
                ),
            )
            .order_by("id")
        )
        return query_set
