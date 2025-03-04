from rest_framework import serializers

from chat.models import ExtendUser


class ExtendUserModelSerializer(serializers.ModelSerializer):
    pear_to_pear_group = serializers.CharField()

    class Meta:
        model = ExtendUser
        fields = [
            "id",
            "username",
            "channel_name",
            "pear_to_pear_group",
            "image",
        ]
