from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user_related:create')
TOKEN_URL       = reverse('user_related:token')
ME_URL          = reverse('user_related:me')

def create_test_user(**params):
	return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
	"""e.g. create user that doesn't require authentication"""

	def setUp(self):
		self.client = APIClient()

	def test_created_user_successfully(self):
		"""Tests user creation success if valid payload is passed"""
		payload = {
		'email'    : 'testing@gmail.com',
		'name'     : 'SourabhTesting',
		'password' : 'Testing@123'
		}
		res = self.client.post(CREATE_USER_URL,payload)
		self.assertEqual(res.status_code,status.HTTP_201_CREATED)
		user = get_user_model().objects.get(**res.data)
		self.assertTrue(user.check_password(payload['password']))
		self.assertNotIn('password',res.data)

	def test_user_exists(self):
		"""Testing to verify that doesnot support duplicate users"""
		payload = {
		'email'    : 'testing@gmail.com',
		'name'     : 'SourabhTesting',
		'password' : 'Testing@123'
		}
		create_test_user(**payload) #creating a user with payload
		res = self.client.post(CREATE_USER_URL,payload) #again tring to create the same  user
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

	def test_password_too_short(self):
		"""Test for password validations"""
		payload = {
		'email'     : 'testing@gmail.com',
		'password'  : 'col-sm',
		}
		res = self.client.post(CREATE_USER_URL,payload) #again tring to create the same  user
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
		# Every single tests cleans the db so the above test will not affect this
		user_exists = get_user_model().objects.filter(
						email=payload['email']
						).exists()
		self.assertFalse(user_exists)
		print("woahhh user_related password too small passed")


	def test_create_token_for_user(self):
		"""Tests that a token is created for users"""
		payload = {
		'email'    : 'testing@sourabh.com',
		'password' : 'MbeforeL'
		}
		create_test_user(**payload)
		res = self.client.post(TOKEN_URL,payload)
		self.assertIn('token',res.data)
		self.assertEqual(res.status_code,status.HTTP_200_OK)

	def test_create_token_with_invalid_credentials(self):
		"""Token should not be provided"""
		create_test_user(email="testing@sourabh.com",password="Testpass123")
		payload = {'email':'testing@sourabh.com','password':'MbeforeL'}
		res     = self.client.post(TOKEN_URL,payload)
		self.assertNotIn('token',res.data)
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

	def test_no_user_then_no_token(self):
		"""If the user doesn't exists then no token"""
		payload = {'email':'testing@sourabh.com','password':'Testpass123'}
		res     = self.client.post(TOKEN_URL,payload)
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

	def test_token_not_provided(self):
		"""If no password,token then no work"""
		payload = {
		'email'   : 'testing@sourabh.com',
		'password': ' '
		}
		res = self.client.post(TOKEN_URL,payload)
		self.assertNotIn('token',res.data)
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

	def test_retrieve_user_unauthorized(self):
		"""Authentication required for users"""
		res = self.client.get(ME_URL) 
		#called without token so should not be allowed
		self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)



class PrivateUserAPITests(TestCase):
	"""Test API requests that requires authentication"""
	def setUp(self):
		self.user = create_test_user(
			email    = 'testing@sourabh.com',
			name     = 'sourabh',
			password = 'MbeforeL'
			)
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)

	def test_retrieve_profile_successfull(self):
		"""Tries to retrieve profile section"""
		res = self.client.get(ME_URL)
		self.assertEqual(res.data,{
			'name':self.user.name,
			'email':self.user.email
			})

	def test_post_not_allowed_at_me(self):
		res = self.client.post(ME_URL,{})
		self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)


	def test_profile_update_working(self):
		"""Test it works but only for authenticated users"""
		payload = {'name':'newname','password':'newpass123'}
		res     = self.client.patch(ME_URL,payload)
		self.user.refresh_from_db()
		self.assertEqual(self.user.name,payload['name'])
		self.assertTrue(self.user.check_password(payload['password']))
		self.assertEqual(res.status_code,status.HTTP_200_OK)