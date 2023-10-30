# from rest_framework import serializers
# from .models import Author

# class AuthorSerializer(serializers.ModelSerializer):
#     # create a serializer for the Post model
   
#     class Meta:
#         model = Author
#         fields = '__all__'

#     def create(self, validated_data):
#         print(validated_data)
#         # Create and return a new `Post` instance, given the validated data
#         return Author.objects.create(**validated_data)

#     def delete(self, instance):
#         # delete a specific post
#         instance.delete()
#         return instance
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'])
		user_obj.username = clean_data['username']
		user_obj.save()
		return user_obj
		

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		# print(user.user_id)
		if not user:
			raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('user_id', 'email', 'username')