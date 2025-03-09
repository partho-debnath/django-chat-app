from django.contrib import admin


from .models import (
    ExtendUser,
    Friendship,
    Messages,
    Groups,
)


@admin.register(ExtendUser)
class ExtendUserModelAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "channel_name",
        "get_full_name",
        "id",
        "is_online",
        "my_group_name",
    ]


@admin.register(Friendship)
class FriendsModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "group__name",
        "person",
        "friend",
    ]


@admin.register(Messages)
class MessagesModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "sender",
        "receiver",
        "message",
        "is_delivered",
        "is_seen_by_receiver",
        "created_at",
        "updated_at",
    ]


@admin.register(Groups)
class GroupsModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]
