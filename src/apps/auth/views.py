from rest_framework import generics
from .serializers import RegisterUserSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer