from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

#from this module imports(Recipie)
from ..models import Ingredient
from ..serializers import IngredientSerializer

#From others module
from core import models

INGREDIENT_URL = reverse('recipie:ingredient-list')


class PublicIngredientAPITest(TestCase):

	def setUP(self):
		self.client = APIClient()

	def test_login_required(self):
		res = self.client.get(INGREDIENT_URL)
		self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsAPITest(TestCase):

	def setUp(self):
		self.client = APIClient()

		self.user   = get_user_model().objects.create_user(
						'testing@so.com',
						'TestPass123'
						)
		self.client.force_authenticate(self.user)

	def test_retrieve_ingredient_list(self):
		"""Test  retriving a list of Ingredients"""
		Ingredient.objects.create(user = self.user,name = "Lemon")
		Ingredient.objects.create(user = self.user,name = "Chilly")
		res = self.client.get(INGREDIENT_URL)
		ingredients = Ingredient.objects.all().order_by('-name')
		serializer  = IngredientSerializer(ingredients,many=True)
		self.assertEqual(res.status_code,status.HTTP_200_OK)
		self.assertEqual(res.data,serializer.data)

		def test_ingredients_limited_to_user(self):
			"""Test that ingredients for the authenticated user are returend"""
			user2 = get_user_model().objects.create_user(
														'other@londonappdev.com',
														'testpass'
														)
			Ingredient.objects.create(user=user2, name='Vinegar')
			ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

			res = self.client.get(INGREDIENTS_URL)

			self.assertEqual(res.status_code, status.HTTP_200_OK)
			self.assertEqual(len(res.data), 1)
			self.assertEqual(res.data[0]['name'], ingredient.name)