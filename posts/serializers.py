from rest_framework import serializers
from users.serializers import GetAllUsersSerializer
from .models import Post
from users.models import User


class PostSerializer(serializers.ModelSerializer):
    author = GetAllUsersSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('id', 'message', 'timestamp', 'author')
