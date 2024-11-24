from django.utils import timezone
from rest_framework import generics,status,exceptions
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    VerifyLoginOTPSerializer,
    UserSerializer,
    UserChangePasswordSerializer,
    ForgotPasswordSerializer,
    VerifyForgotPasswordSerializer,
    ChangeForgotPasswordSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Device
from src.apps.common.utills import get_user_ip
from src.apps.common.otp import OTPhandlers,OTPAction
import geocoder
import logging

logger = logging.getLogger('info_logger')

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        logger.info(f'User created: {serializer.data["username"]}')
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
                logger.info(f'{user.username} device information updated')
            except Device.DoesNotExist:
                device = Device.objects.create(
                    user = user,
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
                logger.info(f'{user.username} device information created')

            logger.info(f'{user.username} logged in')
            
            return Response({'refresh':str(token),'access': str(token.access_token),'msg':'User logged in successful'},status=status.HTTP_200_OK)
        else:
            otp_handler = OTPhandlers(request,user,OTPAction.LOGIN)
            otp_handler.send_otp()
    
            logger.info(f'Login otp sent to: {user.username}')
            return Response({'msg':'Login OTP has been sent to your email address'},status=status.HTTP_200_OK)
        

class VerifyLoginOTPView(generics.GenericAPIView):

    serializer_class = VerifyLoginOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user',None)

        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)
            logger.info(f'User login otp verified: {user.username}')

            user.is_active = True
            user.last_login = timezone.now()
            user.save()

            return Response(
                {
                   'refresh':str(token),
                    'access': str(token.access_token),
                   'msg':'OTP verified successfully'
                },
                status=status.HTTP_200_OK
            )
        
        logger.warning(f'User login otp verification failed')
        return Response({'msg':'OTP verification failed'},status=status.HTTP_400_BAD_REQUEST)
    

class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exceptions=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = serializer.validated_data.get('refresh')
        if refresh_token is None:
            logger.warning('Refresh token not found')
            raise exceptions.APIException({'error': 'Refresh token is required'},status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        try:
            token.blacklist()
            user = request.user
            user.status = False
            user.save()
            logger.info(f'{user.username} logged out successfully')
            return Response({'msg':'User logged out successful'},status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.warning(f'User logout failed: {str(e)}')
            raise exceptions.APIException({'error': str(e)},status=status.HTTP_400_BAD_REQUEST)

class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs.get('pk', None)
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise exceptions.APIException({'error': 'User does not exist'})
        
        return user
    
    def get_queryset(self):
        return User.objects.all()

class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def get_queryset(self):
        return User.objects.all()
    
    
class UserlistView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
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
    
    
class UserChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user',None)

        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)

            logger.info(f'User password changed successfully: {user.username}')

            return Response(
                {
                   'refresh':str(token),
                    'access': str(token.access_token),
                   'msg':'Password changed successfully'
                },
                status=status.HTTP_200_OK
            )
        
        logger.info(f'User password change unsuccessfull: {user.username}')
        return Response({'msg':'Password not changed'},status=status.HTTP_200_OK)
    

class ForgotPasswordView(generics.GenericAPIView):

    serializer_class = ForgotPasswordSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user',None)

        if user is not None:
            otp_handler = OTPhandlers(request,user,OTPAction.RESET)
            otp_handler.send_otp()

            logger.info(f'User forgot password otp sent: {user.username}')

            return Response({'msg':'Reset OTP has been sent to your email address'},status=status.HTTP_200_OK)

        logger.info(f'User forgot password otp send unsuccessful: {user.username}')
        return Response({'msg':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    

class VerifyForgotPasswordView(generics.GenericAPIView):

    serializer_class = VerifyForgotPasswordSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message = serializer.validated_data.get('message',None)
        
        logger.info(f'User forgot password otp sent: {serializer.validated_data.get("user").username}')

        return Response({'msg':message},status=status.HTTP_200_OK)
    

class ChangeForgotPasswordView(generics.GenericAPIView):

    serializer_class = ChangeForgotPasswordSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user',None)

        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)

            logger.info(f'User password changed successfully: {user.username}')
            return Response(
                {
                   'refresh':str(token),
                    'access': str(token.access_token),
                   'msg':'Password changed successfully'
                },
                status=status.HTTP_200_OK
            )
        
        logger.info(f'User password changed unsuccessfully')
        return Response({'msg':'Password not changed'},status=status.HTTP_200_OK)