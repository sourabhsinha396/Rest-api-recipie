from django.shortcuts import render

from rest_framework import viewsets,mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import TagSerializer,IngredientSerializer
from .models import Tag,Ingredient

class TagViewset(viewsets.GenericViewSet,
				mixins.ListModelMixin,
				mixins.CreateModelMixin):
	authentication_classes = (TokenAuthentication,)
	permission_classes     = (IsAuthenticated,)
	queryset               = Tag.objects.all()
	serializer_class       = TagSerializer

	def get_queryset(self):
		"""Return only tags for authenticated user"""
		return self.queryset.filter(user=self.request.user).order_by('-name')

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)
		

class IngredientViewset(viewsets.GenericViewSet,mixins.ListModelMixin):
	authentication_classes = (TokenAuthentication,)
	permission_classes     = (IsAuthenticated,)
	queryset               = Ingredient.objects.all()
	serializer_class       = IngredientSerializer

	def get_queryset(self):
		"""Return objects only for current auth user"""
		return  self.queryset.filter(user = self.request.user).order_by('-name')