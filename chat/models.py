from django.db import models
from django.contrib.auth.models import AbstractUser


class ExtendUser(AbstractUser):
    is_online = models.BooleanField(default=False)
    channel_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.email} -> {self.channel_name}"


class Friends(models.Model):
    person = models.ForeignKey(
        to=ExtendUser,
        on_delete=models.CASCADE,
        related_name="persons",
    )
    friend = models.ForeignKey(
        to=ExtendUser,
        on_delete=models.CASCADE,
        related_name="friends",
    )
