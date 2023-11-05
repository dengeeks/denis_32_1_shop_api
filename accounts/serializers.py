from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import ConfirmUser


class CreateAccountValidate(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise serializers.ValidationError(f'Account with {email} already exists')

    def validate_username(self, username):
        try:
            User.objects.get(email=username)
        except User.DoesNotExist:
            return username
        raise serializers.ValidationError(f'Account with {username} already exists')


class LoginValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()


class ConfirmUserSerializer(serializers.Serializer):
    code = serializers.CharField()
    user = None

    def validate_code(self, code):
        try:
            user = User.objects.get(user_confirm__code=code)
            self.user = user
            time = (timezone.now() - user.user_confirm.created).seconds
            if time > 120:
                user.delete()
                raise serializers.ValidationError('Time is over')
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid code, You have 120 seconds to confirm account')
        return code
