from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    # create a serializer for the Post model
    class Meta:
        model = Post
        fields = '__all__'

    # when a GET request is made, use the comments field and the CommentSerializer to return the comments
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        comments = Comment.objects.filter(postId=instance.id).all()
        if comments is not None:
            # get all comments with postId = instance.id and the number of comments returned (count)
            representation['comments'] = CommentSerializer(comments, many=True).data
            representation['count'] = len(comments)
        return representation

    def create(self, validated_data):
        # Create and return a new `Post` instance, given the validated data
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update and return an existing `Post` instance, given the validated data
        instance.title = validated_data.get('title', instance.title)
        instance.caption = validated_data.get('caption', instance.caption)
        instance.image = validated_data.get('image', instance.image)
        instance.categories = validated_data.get('categories', instance.categories)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        instance.save()
        return instance
    
    def delete(self, instance):
        # delete a specific post
        instance.delete()
        return instance
    

class CommentSerializer(serializers.ModelSerializer):
    # create a serializer for the Comment model
    class Meta:
        model = Comment
        fields = ['id', 'author', 'comment', 'contentType', 'published', 'postId']

    def create(self, validated_data):
        # Create and return a new `Comment` instance, given the validated data
        return Comment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update and return an existing `Comment` instance, given the validated data
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance
    
    def delete(self, instance):
        # delete a specific comment
        instance.delete()
        return instance