from django.urls import path
from .views import (
    CreateUserView, 
    UserLoginView, 
    UserLogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    PasswordResetTokenVerifyView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('', CreateUserView.as_view(), name = "index"),
    path('login', UserLoginView.as_view(), name="login"),
    path('logout', UserLogoutView.as_view(), name='logout'),

    # Password reseting
    path('password-reseting', PasswordResetRequestView.as_view(),name='reset-passwor' ),
    path('password-reset/confirm', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/verify-token', PasswordResetTokenVerifyView.as_view(), name='verify-token'),

    #JWT endpoint
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
