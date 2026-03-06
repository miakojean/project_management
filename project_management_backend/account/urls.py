# dans account/urls.py
from django.urls import path
from .views import (
    CreateUserView, 
    UserLoginView, 
    UserLogoutView, 
    PasswordResetRequestView,
    PasswordResetTokenVerifyView,
    PasswordResetConfirmView,
    UserProfileView,
    CustomTokenRefreshView
)

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/verify/', PasswordResetTokenVerifyView.as_view(), name='password-reset-verify'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]