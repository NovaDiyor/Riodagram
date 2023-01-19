from rest_framework import serializers
from .models import *


class ChatOne(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class StoryOne(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = '__all__'


class PostOne(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'


class CommentOne(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Comment
        fields = '__all__'


class FollowOne(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class UserVisible(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'img', 'bio']


class ContentOne(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
