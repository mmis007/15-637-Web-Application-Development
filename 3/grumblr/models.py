from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):

    user = models.ForeignKey(User)
    text = models.TextField(max_length=42)
    date = models.DateTimeField(
            default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


