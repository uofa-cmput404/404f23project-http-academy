from rest_framework import serializers
from .models import Post, Comment, Category

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
        categories = Category.objects.filter(postId=instance.id).all()
        if categories is not None:
            # get all categories with postId = instance.id and the number of categories returned (count)
            categoryList = []
            for category in categories:
                # get the category name for each category
                categoryList.append(category.category)
            representation['categories'] = categoryList

        return representation

    def create(self, validated_data):
        # parse the categories from the validated data
        categories = validated_data.pop('categories')
        for category in categories:
            # for each category, create a new Category object and save it
            newCategory = Category(category=category)
            newCategory.save()
        # Create and return a new `Post` instance, given the validated data
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update and return an existing `Post` instance, given the validated data
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.categories = validated_data.get('categories', instance.categories)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        instance.save()
        return instance
    
    def updateCategories(self, instance, validated_data):
        # Update and return an existing `Post` instance, given the validated data
        categories = validated_data.get('categories', instance.categories)
        for category in categories:
            # for each category, create a new Category object and save it
            newCategory = Category(category=category, postId=instance)
            newCategory.save()
        instance.categories = categories
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


class CategorySerializer(serializers.ModelSerializer):
    # serializer for the Category model
    class Meta:
        model = Category
        fields = ['id', 'category', 'postId']
    
    def create(self, validated_data):
        # Create and return a new `Category` instance, given the validated data
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update and return an existing `Category` instance, given the validated data
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

    def delete(self, instance):
        # delete a specific category
        instance.delete()
        return instance