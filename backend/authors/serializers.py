from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from .models import AppUser

UserModel = AppUser


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, clean_data):
        if clean_data.get("isForeign"):
            foreign_id = clean_data.get("id").split("/").pop()

            user_obj = AppUser.objects.create(
                email=clean_data["email"],
                username=clean_data.get("username", ""),
                displayName=clean_data.get("displayName", ""),
                github=clean_data.get("github", ""),
                profileImage=clean_data.get("profileImage", ""),
                isForeign=True,  # Set isForeign to True
                foreign=foreign_id,  # Set foreign field
            )
        else:
            user_obj = AppUser.objects.create(
                email=clean_data["email"],
                username=clean_data.get("username", ""),
                displayName=clean_data.get("displayName", ""),
                github=clean_data.get("github", ""),
                profileImage=clean_data.get("profileImage", ""),
                isForeign=False,  # Set isForeign to false
            )
        user_obj.set_password(clean_data["password"])
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    ##
    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data["email"], password=clean_data["password"]
        )
        # print(user.user_id)
        if not user:
            raise ValidationError("user not found")
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "email",
            "username",
        )  # add any other fields you want to allow updating

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "type",
            "id",
            "url",
            "host",
            "displayName",
            "foreign",
            "github",
            "profileImage",
        )
