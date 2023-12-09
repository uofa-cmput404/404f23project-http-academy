from rest_framework import serializers
from .models import Post, Comment, Like
import uuid


class PostSerializer(serializers.ModelSerializer):
    # create a serializer for the Post model

    class Meta:
        model = Post
        fields = '__all__'

    # when a GET request is made, use the comments field and the CommentSerializer to return the comments
    def to_representation(self, instance):
        commentRepresentation = super().to_representation(instance)
        comments = Comment.objects.filter(postId=instance.post_id).all()
        if comments is not None:
            # get all comments with postId = instance.id and the number of comments returned (count)
            commentRepresentation['comments'] = CommentSerializer(
                comments, many=True).data
            commentRepresentation['count'] = len(comments)

        return commentRepresentation

    # def create(self, validated_data):
    #     # post = Post.objects.create(**validated_data)
    #     user = validated_data.get('author')

    #     """
    #     create posts for foreign authors
    #     1. i want to try and get the user being set in in the user field
    #     2. if the user is a foreign author then create post for them using their uuid
    #     """
    #     if user.isForeign:
    #         post = Post.objects.create(**validated_data, author = )

    #     post_id = str(post.post_id)  # Use the auto-generated UUID
    #     post.id = post_id
    #     post.url = user.url + "/posts/" + post_id
    #     post.save()
    #     return post

    def create(self, validated_data):
        user = validated_data.get('author')

        print('validated data from front end', validated_data)
        # Create a new post instance without saving it to the database yet
        post = Post(**validated_data)
        image_url = validated_data.pop('image_url', None)
        print('post field', post.image_url)
        try:
            # Check if the user is a foreign author
            if user.isForeign:
                # Extract the foreign post ID from the user's URL
                post_foreign_id = user.url.split('/')[-1]
                post.id = f"{user.url}/posts/{post_foreign_id}/"
                post.foreign = post_foreign_id
                post.url = user.url + "/posts/" + post.id
            else:
                # Generate the id for a local author
                post.id = f"{user.host}authors/{user.pk}/posts/{post.post_id}/"
                post.url = user.url + "/posts/" + post.id

            if not post.image_url:
                print('hit this to create')
                post.image_url = None
            # Save the post instance
            post.save()
            return post

        except Exception as e:
            # Log the exception or handle it as needed
            print(f"Error in creating post: {str(e)}")
            return {'status': f'failed to create post: {str(e)}'}

    def update(self, instance, validated_data):
        # Update and return an existing `Post` instance, given the validated data
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.categories = validated_data.get(
            'categories', instance.categories)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.likes = validated_data.get('likes', instance.likes)
        instance.visibility = validated_data.get(
            'visibility', instance.visibility)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        instance.image_url = validated_data.get('image_url', instance.image_url)
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
        fields = ['id', 'author', 'comment',
                  'contentType', 'published', 'postId']

    def create(self, validated_data):
        # Create and return a new `Comment` instance, given the validated data
        user = validated_data.get('author')

        # Create a new post instance without saving it to the database yet
        comment = Comment(**validated_data)
        try:
            # Check if the user is a foreign author
            if comment.isForeign:
                # Extract the foreign post ID from the user's URL
                comment_foreign_id = comment.url.split('/')[-1]
                comment_url = str(comment.postId.id) + \
                    "comments/" + str(comment.comment_id)
                comment.id = comment_url
                comment.url = comment.id
                comment.foreign = comment_foreign_id

            else:
                comment_url = str(comment.postId.id) + \
                    "comments/" + str(comment.comment_id)
                comment.id = comment_url
                comment.url = comment.id
                print('comment field', comment.id)
                print('comment field', comment.author)
                print('comment field', comment.url)
                print('comment field', comment.isForeign)
                print('comment field', comment.foreign)
            # Save the post instance
            comment.save()
            return comment

        except Exception as e:
            # Log the exception or handle it as needed
            print(f"Error in creating post: {str(e)}")
            return {'status': f'failed to create post: {str(e)}'}

    def update(self, instance, validated_data):
        # Update and return an existing `Comment` instance, given the validated data
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

    def delete(self, instance):
        # delete a specific comment
        instance.delete()
        return instance


# class PostLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = ['id', 'author', 'postId', 'like']


# for liking comments later on
class CommentLikeSerializer(serializers.ModelSerializer):
    author_displayName = serializers.CharField(source='author.displayName')
    author_id = serializers.UUIDField(source='author.user_id')

    class Meta:
        model = Like
        fields = ['id', 'author_displayName', 'author_id', 'commentId']

    # def get_author_id(self, obj):
    #     return obj.author.user_id
