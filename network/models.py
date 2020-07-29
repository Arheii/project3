from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    folowing = models.ManyToManyField('User', blank=True, related_name='folowers')
    pass


class Tweet(models.Model):
    # title = models.CharField(max_length=32)
    body = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    likes = models.ManyToManyField(User, blank=True, related_name='favs')

    def __str__(self):
        return f'{self.owner}: {self.body[:50]}'

    class Meta:
        ordering = ['-created_on']