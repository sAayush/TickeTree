from .models import *
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from utils.utils import create_login_response, create_response
from .serializers import UserSerializer, RegisterUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class LoginUserView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                # Get user details
                user = User.objects.get(email=request.data.get('email'))
                user_data = UserSerializer(user).data
                
                # Prepare token response
                token_data = {
                    "access": response.data['access'],
                    "refresh": response.data['refresh']
                }
                
                return create_login_response(
                    status="success",
                    message="Login successful",
                    token=token_data,
                    status_code=status.HTTP_200_OK
                )
        except Exception as e:
            return create_login_response(
                status="error",
                message="Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            
class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                return create_response(
                    status="success",
                    message="Token refreshed successfully",
                    data={"access": response.data['access']},
                    status_code=status.HTTP_200_OK
                )
        except Exception as e:
            return create_response(
                status="error",
                message="Invalid refresh token",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

class RegisterUserView(APIView):
    serializer_class = RegisterUserSerializer
    parser_classes = (JSONParser,)

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.create_user(
                    email=serializer.validated_data['email'],
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password'],
                    user_type='user'
                )
                
                # Generate tokens manually
                token = TokenObtainPairSerializer().get_token(user)
                
                # Prepare token data
                token_data = {
                    "access": str(token.access_token),
                    "refresh": str(token)
                }
                
                user_data = UserSerializer(user).data
                return create_response(
                    status="success",
                    message="User registered successfully",
                    data={"token": token_data, "user": user_data},
                    status_code=status.HTTP_201_CREATED
                )
            except Exception as e:
                return create_response(
                    status="error",
                    message=str(e),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        return create_response(
            status="error",
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class UserListCreateView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer