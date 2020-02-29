from rest_framework.serializers import ModelSerializer, ValidationError, Serializer, CharField
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
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
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class LoginSerializer(Serializer):
    username = CharField()
    password = CharField()




