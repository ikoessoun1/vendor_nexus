# users/serializers.py
from rest_framework import serializers
from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'unit', 'department', 'password']

    def validate_email(self, value):
        return value.lower()

    def validate_first_name(self, value):
        return value.lower()

    def validate_last_name(self, value):
        return value.lower()

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = True  # This makes them admin-level
        user.save()
        return user
