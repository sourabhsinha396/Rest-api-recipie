from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
	"""This tests deals with user creation,using email"""
	def test_create_user_with_email_working(self):
		email    = "testing@gmail.com"
		password = "Testpass123"

		user     = get_user_model().objects.create_user(
					email=email,
					password=password
					)
		self.assertEqual(user.email,email)
		self.assertTrue(user.check_password(password))

	def test_email_normalization_working(self):
		'''The second part of email e.g. gmail.com is actually case insensitive'''
		email = "testing@GMAIL.COM"
		user  = get_user_model().objects.create_user(email,'Testpass123')
		self.assertEqual(user.email,email.lower())

	def test_new_user_invalid_email(self):
		"""Test creating user with no email raises error"""
		with self.assertRaises(ValueError):
		    get_user_model().objects.create_user(None, 'test123')
		print("Test 3 OK")

	def test_create_superuser_working(self):
		"""Create superuser working or not"""
		user = get_user_model().objects.create_superuser(
				'testing@gmail.com',
				'Testpass123')
		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)
		print("\nTest 4 OK")
