from django.conf import settings

from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)

from .models import User

class UserViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'login':
            return UserLoginSerializer
        if self.action == 'register':
            return UserRegisterSerializer
        if self.action == 'profile':
            return UserProfileSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'profile':
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            serializer.login()
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(
                key='Bearer',
                value=serializer.token,
                httponly=True,
                domain=settings.DOMAIN
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def register(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def profile(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def logout(self, request):
        response = Response(
            {'logout':True},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('Bearer')
        return response
