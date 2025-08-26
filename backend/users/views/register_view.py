# users/views.py
from rest_framework import generics, permissions
from users.serializers import UserRegistrationSerializer
from users.models import User

class AdminCreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.IsAdminUser]
