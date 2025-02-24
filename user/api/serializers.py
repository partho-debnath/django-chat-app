from rest_framework import serializers

from chat.models import ExtendUser


class ExtendUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExtendUser
        fields = [
            "id",
            "username",
            "channel_name",
        ]
