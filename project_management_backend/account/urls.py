from django.urls import path
from .views import (
    CreateUserView,
    UserLoginView,
    UserLogoutView,
    PasswordResetRequestView,
    PasswordResetTokenVerifyView,
    PasswordResetConfirmView,
    UserProfileView  # Import de la vue existante
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    #path('register', CreateUserView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    
    # JWT Token refresh
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Password reset
    path('password-reset', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/verify', PasswordResetTokenVerifyView.as_view(), name='password_reset_verify'),
    path('password-reset/confirm', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # User profile - AJOUT DE CETTE LIGNE
    path('me', UserProfileView.as_view(), name='user_profile'),
]