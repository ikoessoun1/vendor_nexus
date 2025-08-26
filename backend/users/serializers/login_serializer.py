# users/serializers/login_serializer.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models.user_model import User
from .user_serializer import UserSerializer

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
        else:
            raise serializers.ValidationError("Both username and password are required")

        # Attach user instance for view usage
        attrs["user"] = user
        return attrs

    def to_representation(self, instance):
        # Optional: when returning user info in response
        user = instance.get("user")
        return UserSerializer(user).data
