from django.shortcuts import render
from djoser.views import UserViewSet as DjoserUserViewSet
from .models import User
from .serializers import UserSerializer

class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer