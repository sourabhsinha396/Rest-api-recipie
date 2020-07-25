from django.shortcuts import render

#From rest framework
from rest_framework import generics

#From this module
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
	serializer_class = UserSerializer