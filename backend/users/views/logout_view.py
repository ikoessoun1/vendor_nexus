# users/views/logout_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # With token-in-localStorage, backend doesn't manage logout.
        # Just let frontend clear tokens.
        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)


