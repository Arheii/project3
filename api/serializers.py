from .models import User, Tweet
from rest_framework import serializers


class TweetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tweet
        fields = ['url', 'id', 'title', 'owner', 'create_on', 'likes']

