from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from blog.models import Post, Category, TagPost


class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = '__all__'
