from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Concat


class ExtendUser(AbstractUser):
    is_online = models.BooleanField(default=False)
    channel_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    my_group_name = models.GeneratedField(
        expression=Concat(
            "id",
            models.Value("-"),
            "username",
        ),
        output_field=models.CharField(
            max_length=100,
            blank=True,
            null=True,
        ),
        db_persist=True,
    )
    image = models.ImageField(
        upload_to="profile_pictures",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.email} -> {self.channel_name}"

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["username"]),
        ]


class Friendship(models.Model):
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
    group = models.ForeignKey(
        to="Groups",
        on_delete=models.RESTRICT,
        related_name="group_name",
    )

    class Meta:
        indexes = [
            models.Index(fields=["person"]),
            models.Index(fields=["friend"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "person",
                    "friend",
                ],
                name="person_friend",
            ),
            models.UniqueConstraint(
                fields=[
                    "person",
                    "friend",
                    "group",
                ],
                name="person_friend_group",
            ),
        ]


class Messages(models.Model):
    sender = models.ForeignKey(
        to=ExtendUser,
        on_delete=models.CASCADE,
        related_name="send_messages",
    )
    receiver = models.ForeignKey(
        to=ExtendUser,
        on_delete=models.CASCADE,
        related_name="receive_messages",
    )
    content = models.TextField()
    is_delivered = models.BooleanField(db_default=False)
    is_seen_by_receiver = models.BooleanField(db_default=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )


class Groups(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(
                fields=["name"],
            ),
        ]


class FriendRequest(models.Model):
    person = models.ForeignKey(
        to=ExtendUser,
        on_delete=models.CASCADE,
        related_name="received_friend_requests",
    )
    requested_by = models.ForeignKey(
        to=ExtendUser,
        on_delete=models.CASCADE,
        related_name="sent_friend_requests",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
