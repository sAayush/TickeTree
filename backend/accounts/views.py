from .serializers import *
from rest_framework import generics
from .models import CustomUser, HostProfile
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

class RegisterUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserPostSerializer

    def create(self, request, *args, **kwargs):
        user_type = request.data.get("user_type", "normal")
        user = CustomUser.objects.create_user(
            email=request.data["email"],
            username=request.data["username"],
            password=request.data["password"],
            user_type=user_type
        )
        if user_type == "host":
            HostProfile.objects.create(user=user, organization_name=request.data["organization_name"])
        return Response({"message": "User registered successfully"})

class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserPostSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserPostSerializer