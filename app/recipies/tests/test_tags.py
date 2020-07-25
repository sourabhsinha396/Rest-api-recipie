from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

#from this module imports(Recipie)
from ..models import Tag
from ..serializers import TagSerializer

#From others module
from core import models

TAGS_URL = reverse('recipie:tag-list')

def sample_users(email='testing@sourabh.com',password='Testing123'):
	"""Create a Sample user to use again and again"""
	return get_user_model().objects.create_user(email,password)




class TestTags(TestCase):

	def test_tag_str(self):
		"""Test that tag module is making object successfully"""
		tag = Tag.objects.create(
			user = sample_users(),
			name = 'Tomato'
			)
		self.assertEqual(str(tag),tag.name)

class PublicTagsAPITest(TestCase):

	def setUp(self):
		self.client = APIClient()

	def test_login_required(self):
		"""Test login_req to retrieve tags"""
		res = self.client.get(TAGS_URL)
		self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):

	def setUp(self):
		self.user  = get_user_model().objects.create_user(
			'testing@sourabh.com',
			'Testing123'
			)
		self.client = APIClient()
		self.client.force_authenticate(self.user)

	def test_retrieve_tags(self):
		Tag.objects.create(user = self.user,name = "Tomato")
		Tag.objects.create(user = self.user,name = "Chilly")
		res = self.client.get(TAGS_URL)

		tags= Tag.objects.all().order_by('-name')
		serializer = TagSerializer(tags,many=True) 
		# trying to serialize more than one items then many=True
		self.assertEqual(res.status_code,status.HTTP_200_OK)
		self.assertEqual(res.data,serializer.data)

	def test_tags_limited_to_auth_user(self):
		"""Test that users doesn't get others tags"""
		user2 = get_user_model().objects.create_user(
			'testing2@sourabh.com',
			'MbeforeL'
			)
		Tag.objects.create(user = user2,name="Lemon Chilly")
		tag = Tag.objects.create(user=self.user,name="panda egg")
		res = self.client.get(TAGS_URL)
		self.assertEqual(res.status_code,status.HTTP_200_OK)
		self.assertEqual(len(res.data),1)  # only self.users should be present
		self.assertEqual(res.data[0]['name'],tag.name)
	
	######_------------------------#############
	def test_create_tag_successful(self):
		"""Test creating a new tag"""
		payload = {'name':'Tomato'}
		self.client.post(TAGS_URL,payload)
		exists = Tag.objects.filter(user = self.user,name=payload['name']).exists()
		self.assertTrue(exists)

	def test_creating_tag_with_invalid_fails(self):
		payload = {'name':''}
		res     = self.client.post(TAGS_URL,payload)
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)