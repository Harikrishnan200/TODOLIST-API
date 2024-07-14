from django.shortcuts import render
from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer

# class CustomUserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import CustomUser
from .serializers import ForgotPasswordSerializer

from .serializers import ResetPasswordSerializer

class RegisterView(APIView):

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# JSON for register
# {
#     "email": "user@example.com",
#     "first_name": "John",
#     "last_name": "Doe",
#     "password": "password123"
# }


#JSON for login
# {
#     "email": "user@example.com",
#     "password": "password123"
# 
# }

class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)
            
            # Generate a random token (you might want to use a more secure method in production)
            token = get_random_string(length=32)
            
            # Here you would store the token in the database associated with the user
            # This example skips the database part for simplicity
            user.password_reset_token = token
            user.save()

            # Send password reset email
            reset_link = f"http://your-frontend-url/reset-password/{token}"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'hari2003pc@gmail.com',
                [email],
                fail_silently=False,
            )

            return Response({"message": "Password reset link has been sent to your email address."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py
class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            user = CustomUser.objects.get(password_reset_token=token)
            user.set_password(new_password)
            user.password_reset_token = None  # Clear the token
            user.save()

            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
