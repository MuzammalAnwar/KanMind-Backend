from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=255)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_boards",
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="BoardMember",
        related_name="boards",
        blank=True,
    )

    def __str__(self):
        return self.title


class BoardMember(models.Model):
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="memberships")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="board_memberships")
