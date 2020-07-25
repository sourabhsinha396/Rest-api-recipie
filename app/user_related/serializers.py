from django.contrib.auth import get_user_model,authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model  = get_user_model()
		fields = ['email','name','password']
		extra_kwargs = {'password':{'write_only':True,'min_length':7}}

	def create(self,validated_data):
		"""Over-riding the create function"""
		return get_user_model().objects.create_user(**validated_data)

	def update(self,instance,validated_data):
		"""Setting the password using hashing"""
		password = validated_data.pop('password',None)
		# After retriving password it removes it from original dictionary
		user     = super().update(instance,validated_data)
		if password:
			user.set_password(password)
			user.save()
		return user

class AuthTokenSerializer(serializers.Serializer):
	"""Serilizer for user authentication """
	email    = serializers.CharField()
	password = serializers.CharField(
		style = {'input_type':'password'},
		trim_whitespace = False 
		)
	def validate(self,attrs):
		"""Validates and authenticate the user"""
		email    = attrs.get('email')
		password = attrs.get('password')

		user = authenticate(
			request = self.context.get('request'),
			username= email,
			password= password
			)
		if not user:
			msg = _('Unable to authenticate with provided credentials')
			raise serializers.ValidationError(msg,code ='authentication')

		attrs['user'] = user 
		return attrs
