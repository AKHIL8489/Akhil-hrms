from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer,LoginSerializer,LogoutSerializer
from django.http import JsonResponse
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import *
import json

# Create your views here.



class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return JsonResponse({
            "message":"User registered successfully",
            "data":user_data
        },
        status=  status.HTTP_201_CREATED
        )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse({
            "message":"User logged in successfully",
            "data":serializer.data,
        },
        status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def send_otp(request):
    email = request.data.get('email')
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "User not found with this email"}, status=status.HTTP_404_NOT_FOUND)
    
    otp = get_random_string(length=4, allowed_chars='1234567890')
    cache.set(email, otp, timeout=300)
    
    subject = 'Password Reset OTP'
    message = f'Your OTP for password reset is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
    return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def confirm_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    cached_otp = cache.get(email)
    if cached_otp is None or cached_otp != otp:
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    
    if password != confirm_password:
        return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
    
    cached_otp = cache.get(email)
    if cached_otp is None:
        return Response({"message": "OTP expired or not requested"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "User not found with this email"}, status=status.HTTP_404_NOT_FOUND)
    
    user.set_password(password)
    user.save()
    
    cache.delete(email)
    
    subject = 'Password changed'
    message = f'Your password has been changed successfully,your new password is {password}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)


class AddEmployeeView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()