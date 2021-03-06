import random
import string
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


def get_valid_till():
    return timezone.now() + timedelta(days=1)


# generate random string django
def generate_random_string(length=20):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


class ActiveChannel(models.Model):
    channel = models.CharField(max_length=100)
    info = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)


class WSAuth(models.Model):
    info = models.TextField()
    token = models.CharField(default=generate_random_string, max_length=31)
    valid_till = models.DateTimeField(default=get_valid_till)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)


class ChatRoom(models.Model):
    chat_name = models.CharField(max_length=100, unique=True, blank=True,
                                 default=generate_random_string, null=True)
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
