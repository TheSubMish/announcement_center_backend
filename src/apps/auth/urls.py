from django.urls import path

from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserDetailsView,
    UserlistView,
    UserUpdateView,
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register-api'),
    path('login/', UserLoginView.as_view(), name='user-login-api'),
    path('logout/', UserLogoutView.as_view(), name='user-logout-api'),
    path('details/', UserDetailsView.as_view(), name='user-details-api'),
    path('list/', UserlistView.as_view(), name='user-list-api'),
    path('update/', UserUpdateView.as_view(), name='user-update-api'),
]