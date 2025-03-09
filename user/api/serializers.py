from rest_framework import serializers

from chat.models import ExtendUser, Messages


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


class MessagesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Messages
        fields = [
            "id",
            "sender_id",
            "receiver_id",
            "message",
            "is_delivered",
            "is_seen_by_receiver",
            "created_at",
            "updated_at",
        ]
