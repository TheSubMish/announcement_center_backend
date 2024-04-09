from django.utils import timezone
from rest_framework import generics,status,exceptions
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    UserSerializer,
    UserChangePasswordSerializer
)
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Device
from src.apps.common.utills import get_user_ip
import geocoder


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'msg':'User registration successful'},status=status.HTTP_201_CREATED,headers=headers)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user',None)

        user_ip = geocoder.ip(str(get_user_ip(self.request)))

        if Device.objects.filter(device_ip=str(get_user_ip(self.request)), blacklist_ip=True).exists():
            raise exceptions.APIException('Device is backlisted')
        
        if user.email_verified:
            user.is_active = True
            user.last_login = timezone.now()
            user.save()
            token = TokenObtainPairSerializer.get_token(user)

            try:
                device : Device = Device.objects.get(device_ip=user_ip)
                device.device_type = self.request.user_agent.device.family
                device.location=f"{user_ip.city},{user_ip.state},{user_ip.country}"
                device.coordinates=f"{user_ip.lat},{user_ip.lng}"
                device.device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}"
                device.browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}"
                device.access_token = str(token.access_token)
                device.refresh_token = str(token)
                device.last_login = timezone.now()
                device.is_active = True
                device.save()
            except Device.DoesNotExist:
                device = Device.objects.create(
                    admin = user,
                    device_ip=str(get_user_ip(self.request)),
                    device_type = self.request.user_agent.device.family, # type:ignore
                    location=f"{user_ip.city},{user_ip.state},{user_ip.country}",
                    coordinates=f"{user_ip.lat},{user_ip.lng}",
                    device_os=f"{request.user_agent.os.family}/{request.user_agent.os.version_string}",
                    browser_type=f"{request.user_agent.browser.family}/{request.user_agent.browser.version_string}",
                    access_token=str(token.access_token),
                    refresh_token=str(token),
                    is_active=True,
                    blacklist_ip=False,
                    last_login=timezone.now()
                )

            return Response({'refresh':str(token),'access': str(token.access_token),'msg':'User logged in successful'},status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Email not verified'},status=status.HTTP_400_BAD_REQUEST)
        

class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exceptions=True)
        refresh_token = serializer.validated_data.get('refresh')

        if refresh_token is None:
            raise exceptions.APIException({'error': 'Refresh token is required'},status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        try:
            token.blacklist()
            user = request.user
            user.is_active = False
            user.save()
            return Response({'msg':'User logged out successful'},status=status.HTTP_200_OK)
        
        except Exception as e:
            raise exceptions.APIException({'error': str(e)},status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def get_queryset(self):
        return User.objects.all()
    
    
class UserlistView(generics.ListAPIView):
    permission_classes = []
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
    

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    def get_queryset(self):
        return User.objects.all()
    
    
class UserChangePasswordView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password changed successfully'},status=status.HTTP_200_OK)
    

