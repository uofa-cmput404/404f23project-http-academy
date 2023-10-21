from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # create a serializer for the Post model
    class Meta:
        model = Post
        fields = ['id', 'user', 'date', 'title', 'content', 'isPublic', 'unlisted']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.isPublic = validated_data.get('isPublic', instance.isPublic)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        instance.save()
        return instance
    
    def delete(self, instance):
        instance.delete()
        return instance