from django.shortcuts import render
from .models import Post, Comment, Like
from django.urls import reverse 
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['GET', 'POST'])
def posts_list(request):
    if request.method == 'POST':
        # if we want to create a new post, use the serializer and save if valid
        serializer = PostSerializer(data=request.data)
      
        print('serializer data', serializer)
        print('request data', request.data)
        print('is valid', serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
    else:
        # if we want to get all posts, use the serializer to return all posts
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)



@api_view(['GET', 'DELETE', 'PATCH'])
def post_detail(request, pk):
    # get the post with the specified ID
    post = Post.objects.get(id=pk)
    print("this is a new post", request.data)
    serializer = PostSerializer(post, many=False)
    # print('this is the post from front end', post.title, post.caption, post.image)
    if request.method == 'DELETE':
        # if we want to delete a post, delete it and return a success message if it exists
        try:
            post.delete()
            return Response('Post deleted successfully')
        except:
            return Response('Post does not exist')
    elif request.method == 'PATCH':
        # if we want to update a post, update it and return a success message if it exists
        try:
            
            # if we try to update any fields not updateable, return an error
            if request.data.get('id') or request.data.get('author') or request.data.get('published') or request.data.get('count') or request.data.get('likes'):
                return Response('Cannot update id, author, published, count, or likes')
            
            serializer.update(post, request.data)
            return Response('Post updated successfully')
        except:
            print('this is the post that also doesnt exxist', post)
            return Response('Post does not exist')
    else:
        # if we want to get a post, use the serializer to return the post
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def comments_list(request, pk):
    if request.method == 'POST':
        # if we want to create a new comment, use the serializer and save if valid
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
    else:
        # if we want to get all comments for a post, use the serializer to return all comments
        comments = Comment.objects.filter(postId=pk)
        serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE', 'PATCH'])
def comment_detail(request, pk):
    # get the comment with the specified ID
    comment = Comment.objects.get(id=pk)
    serializer = CommentSerializer(comment, many=False)

    if request.method == 'DELETE':
        # if we want to delete a comment, delete it and return a success message if it exists
        try:
            comment.delete()
            return Response('Comment deleted successfully')
        except:
            return Response('Comment does not exist')
    elif request.method == 'PATCH':
        # if we want to update a comment, update it and return a success message if it exists
        try:
            # if we try to update any fields not updateable, return an error
            if request.data.get('id') or request.data.get('author') or request.data.get('published') or request.data.get('postId'):
                return Response('Cannot update id, author, published, or postId')
            serializer.update(comment, request.data)
            return Response('Comment updated successfully')
        except:
            return Response('Comment does not exist')
    else:
        # if we want to get a comment, use the serializer to return the comment
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
def like_post(request, pk):
    
    likes = Like.objects.filter(postId=pk)
    print("these are the likes:  ")
    print(likes)
    already_liked = len(likes.filter(author=request.data.get('author'))) > 0
    print(already_liked)
    if request.method == 'POST':
        # if we want to create a new like, use the serializer and save if valid
        serializer = PostLikeSerializer(data=request.data)
        print("is valid: " + str(serializer.is_valid()))
        if serializer.is_valid() and not already_liked:
            serializer.save()
        else:
            return Response(serializer.errors)
    else:
        # if we want to get all likes for a post, use the serializer to return all likes
        serializer = PostLikeSerializer(likes, many=True)
        likes = Like.objects.filter(postId=pk)
    return Response(serializer.data)
    

'''
    # get the post with the specified ID
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        # if we're liking a post, increment the likes and save if valid
        try:
            post.likes += 1
            post.save()
            return Response('Post liked successfully')
        except:
            return Response('Post does not exist')
    elif request.method == 'DELETE':
        # if we're unliking a post, decrement the likes and save if valid
        try:
            post.likes -= 1
            post.save()
            return Response('Post unliked successfully')
        except:
            return Response('Post does not exist')
    else:
        # if we want to get the number of likes for a post, return the number of likes
        likes = post.likes
        return Response(likes)
'''

@api_view(['GET', 'DELETE'])
def like_detail(request, pk, pkLike):
    # get the like with the specified ID
    like = Like.objects.get(postId=pk , id = pkLike)
    serializer = PostLikeSerializer(like, many=False)

    if request.method == 'DELETE':
        # if we want to delete a like, delete it and return a success message if it exists
        try:
            like.delete()
            return Response('Like deleted successfully')
        except:
            return Response('Like does not exist')
    else:
        # if we want to get a like, use the serializer to return the like
        return Response(serializer.data)



@api_view(['GET'])
def get_post_image(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data["image"])