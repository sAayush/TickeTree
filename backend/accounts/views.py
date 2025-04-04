from .models import *
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from utils.utils import create_login_response, create_response
from .serializers import UserSerializer, RegisterUserSerializer, HostUserSerializer, RegisterHostSerializer
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
                
                # Check if user is of type USER
                if user.user_type != 'USER':
                    return create_login_response(
                        status="error",
                        message="Not a regular user account",
                        status_code=status.HTTP_403_FORBIDDEN
                    )
                
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
                    user=user_data,
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
    permission_classes = []  # Add this to remove authentication requirement

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                # Create user with explicit USER type and additional fields
                user = User.objects.create_user(
                    email=serializer.validated_data['email'],
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    user_type='USER'
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

class RegisterHostView(APIView):
    serializer_class = RegisterHostSerializer
    parser_classes = (JSONParser,)
    permission_classes = []  # Add this to remove authentication requirement

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                # Create the user with HOST user_type
                user = User.objects.create_user(
                    email=serializer.validated_data['email'],
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password'],
                    user_type='HOST'  # Explicitly set as HOST
                )
                
                # Create associated host profile from validated data
                host_data = serializer.validated_data.get('host_profile', {})
                host_profile = HostProfile.objects.create(
                    user=user,
                    organization_name=host_data.get('organization_name', ''),
                    address=host_data.get('address', ''),
                    contact_number=host_data.get('contact_number', ''),
                    website=host_data.get('website', ''),
                    description=host_data.get('description', ''),
                )
                
                # Generate tokens
                token = TokenObtainPairSerializer().get_token(user)
                
                # Prepare token data
                token_data = {
                    "access": str(token.access_token),
                    "refresh": str(token)
                }
                
                # Use HostUserSerializer to include host profile data
                user_data = HostUserSerializer(user).data
                return create_response(
                    status="success",
                    message="Host registered successfully",
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

class LoginHostView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Get email and password from request
            email = request.data.get('email')
            password = request.data.get('password')
            
            # Check if user exists and is a host
            user = User.objects.get(email=email)
            if user.user_type != 'HOST':  # Check for HOST type
                return create_response(
                    status="error",
                    message="Not a host account",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            
            # Authenticate via token obtain pair
            token_data = {
                'email': email,
                'password': password
            }
            token_serializer = TokenObtainPairSerializer(data=token_data)
            if token_serializer.is_valid():
                # Generate token
                token = token_serializer.validated_data
                
                # Get user data with host profile
                user_data = HostUserSerializer(user).data
                
                return create_login_response(
                    status="success",
                    message="Host login successful",
                    token=token,
                    user=user_data,
                    status_code=status.HTTP_200_OK
                )
            else:
                raise Exception("Invalid credentials")
        except User.DoesNotExist:
            return create_login_response(
                status="error",
                message="Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return create_login_response(
                status="error",
                message=str(e) if str(e) else "Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED
            )