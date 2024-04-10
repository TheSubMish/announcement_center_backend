from django.urls import path

from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserDetailsView,
    UserRetrieveView,
    UserlistView,
    UserUpdateView,
    VerifyLoginOTPView,
    UserChangePasswordView,
    ForgotPasswordView,
    VerifyForgotPasswordView,
    ChangeForgotPasswordView,
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register-api'),
    path('login/', UserLoginView.as_view(), name='user-login-api'),
    path('logout/', UserLogoutView.as_view(), name='user-logout-api'),
    path('details/', UserDetailsView.as_view(), name='user-details-api'),
    path('retrieve/<uuid:pk>/', UserRetrieveView.as_view(), name='user-retrieve-api'),
    path('list/', UserlistView.as_view(), name='user-list-api'),
    path('update/', UserUpdateView.as_view(), name='user-update-api'),
    path('verify/login/otp/', VerifyLoginOTPView.as_view(),name='user-verify-api'),
    path('change/password/', UserChangePasswordView.as_view(),name='user-change-password-api'),
    path('forgot/password/', ForgotPasswordView.as_view(),name='user-forgot-password-api'),
    path('verify/forgot/password/otp/',VerifyForgotPasswordView.as_view(), name='forgpt-password-verify-api'),
    path('change/forgot/password/',ChangeForgotPasswordView.as_view(), name='user-change-forgot-password-api'),
]