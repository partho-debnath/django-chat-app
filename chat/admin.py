from django.contrib import admin


from .models import ExtendUser, Friends


@admin.register(ExtendUser)
class ExtendUserModelAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "channel_name",
        "get_full_name",
        "id",
        "is_online",
    ]


@admin.register(Friends)
class FriendsModelAdmin(admin.ModelAdmin):
    list_display = [
        "person",
        "friend",
    ]
