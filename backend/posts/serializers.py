from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # create a serializer for the Post model
    class Meta:
        model = Post
        fields = ['id', 'author', 'published', 'title', 'content', 'contentType', 'categories', 'count', 'comments', 'visibility', 'unlisted']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('author', instance.user)
        instance.published = validated_data.get('published', instance.published)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.categories = validated_data.get('categories', instance.categories)
        instance.count = validated_data.get('count', instance.count)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        instance.save()
        return instance
    
    def delete(self, instance):
        instance.delete()
        return instance