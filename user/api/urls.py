from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "user-api"
urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path(
        "online-friends/",
        views.OnlineActiveFriendList.as_view(),
        name="online-active-friends",
    ),
    path(
        "messages/<int:receiver_id>/",
        views.OldMessageList.as_view(),
        name="old-messages",
    ),
]
