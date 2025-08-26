# backend/users/views/login_view.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from rest_framework_simplejwt.tokens import RefreshToken
# from users.serializers.login_serializer import UserLoginSerializer
# from users.serializers import UserSerializer

# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#             "user": UserSerializer(user).data
#         }, status=status.HTTP_200_OK)


# backend/users/views/login_view.py

#This code handles user login, returning a JWT token and setting cookies for access and refresh tokens.
#cookies are set to be HTTP-only and secure, with specified lifetimes.
#Cookies prevent client-side scripts from accessing the tokens, enhancing security. They prevent XSS attacks by ensuring tokens are not exposed to client-side scripts.
#The access token is set to expire after 15 minutes, while the refresh token lasts for
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers.login_serializer import UserLoginSerializer
from users.serializers import UserSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "user": UserSerializer(user).data,
            "access": access_token,
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


