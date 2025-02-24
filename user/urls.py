from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .api import views

app_name = "user"
urlpatterns = [
    path("", obtain_auth_token, name="login"),
    path(
        "online-users/",
        views.OnlineUserList.as_view(),
        name="online",
    ),
]
