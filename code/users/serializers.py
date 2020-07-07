from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from posts.models import Post
from .models import Comment, CommentPhoto, CommentRate


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        try:
            User.objects.get(username=value)
            raise ValidationError('User with such username exist')
        except User.DoesNotExist:
            return value

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
            raise ValidationError('User with such email exist')
        except User.DoesNotExist:
            return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_active=False)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class InitCommentPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    def create(self, validated_data):
        return Comment(post=validated_data['post'])


class CommentPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentPhoto
        fields = ('picture',)

    def create(self, validated_data):
        return CommentPhoto(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        instance.is_released = True
        instance.released_at = timezone.now()
        instance.save()
        return instance

    class Meta:
        model = Comment
        fields = ('content', 'post')

    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)


class CommentRateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return CommentRate(**validated_data)

    class Meta:
        model = CommentRate
        fields = ('like',)


class BookmarkSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
