from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from rest_framework.permissions import IsAuthenticated

from chat.models import ExtendUser


from .serializers import ExtendUserModelSerializer


class OnlineUserList(ListAPIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ExtendUserModelSerializer

    queryset = ExtendUser.objects.filter(
        is_online=True,
    ).values(
        "id",
        "username",
        "channel_name",
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
