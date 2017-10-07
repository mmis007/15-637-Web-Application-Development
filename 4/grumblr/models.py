from django.db import models

from django.contrib.auth.models import User
from django.db.models import CASCADE
from django.utils import timezone


class Post(models.Model):

    user = models.ForeignKey(User)
    text = models.CharField(max_length=42,  default='', blank=True)
    date = models.DateTimeField(
            default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    bio = models.TextField(max_length=420, default='', blank=True)
    age = models.SmallIntegerField(default=0, blank=True)
    photo = models.ImageField(upload_to="img", blank=True)

    follow = models.ManyToManyField(User, related_name="follow_user")

    confirm_token = models.CharField(max_length=100, default='', blank=True)
