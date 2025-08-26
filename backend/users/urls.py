# backend/urls.py
from django.urls import path
from users.views import AdminCreateUserView, LoginView, MeView, LogoutView, RefreshTokenView



urlpatterns = [
  # User management endpoints
  # Admin user creation endpoint
    path('admin/register/', AdminCreateUserView.as_view(), name='admin-register'),

    # User login endpoint
    # This endpoint allows users to log in and receive a token
    path('login/', LoginView.as_view(), name='user-login'),

    # User profile endpoint
    # This endpoint allows authenticated users to view and update their profile
    path('me/', MeView.as_view(), name='user-me'),

    # Token refresh endpoint
    # This endpoint allows users to refresh their access token
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),

    # Logout endpoint
    # This endpoint allows users to log out by blacklisting their refresh token
    path('logout/', LogoutView.as_view(), name='logout'),
]
