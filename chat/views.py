from django.shortcuts import render

from .models import ExtendUser


def index(request):
    users = ExtendUser.objects.select_related("user").only(
        "user",
        "channel_name",
    )
    print(users)
    return render(
        request,
        "chat/index.html",
    )


def room(request, room_name):
    return render(
        request,
        "chat/room.html",
        {
            "room_name": room_name,
        },
    )
