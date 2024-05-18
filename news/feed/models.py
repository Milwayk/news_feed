import django
from django.db import models


class News(models.Model):
    author = models.TextField()
    header = models.TextField()
    theme = models.TextField()
    content = models.TextField()


class Comments(models.Model):
    author = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    comment = models.TextField()
    news_id = models.IntegerField(default=0)