from rest_framework import serializers
from .models import author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = author
        fields = "__all__"

    def create(self, validated_data):
        return author.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.host = validated_data.get('host', instance.host)
        instance.displayName = validated_data.get('displayName', instance.displayName)
        instance.github = validated_data.get('github', instance.github)
        instance.profileImage = validated_data.get('profileImage', instance.profileImage)
        instance.save()
        return instance
    
    def delete(self, instance):
        instance.delete()
        return instance