from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User
from django.utils.translation import ugettext as _

class GetAllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'date_joined', 'email')


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_email(self, email):
        if User.objects.filter(email=email).exists() :
            raise serializers.ValidationError(_("That email is already in use.  Choose another."))
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(_("That username is already in use.  Choose another ."))
        return username

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        return value

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
