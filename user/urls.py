from django.urls import path
from rest_framework.authtoken import views

app_name = "user"
urlpatterns = [
    path("", views.obtain_auth_token, name="login"),
]
