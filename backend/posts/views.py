from django.shortcuts import render
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET', 'POST'])
def posts_list(request):
    if request.method == 'POST':
        # if we want to create a new post, use the serializer and save if valid
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
    else:
        # if we want to get all posts, use the serializer to return all posts
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def post_detail(request, pk):
    # get the post with the specified ID
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)

    if request.method == 'DELETE':
        # if we want to delete a post, delete it and return a success message if it exists
        try:
            post.delete()
            return Response('Post deleted successfully')
        except:
            return Response('Post does not exist')
    else:
        # if we want to get a post, use the serializer to return the post
        return Response(serializer.data)

# TODO: add the ability to PATCH posts

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

@api_view(['GET', 'DELETE'])
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
    else:
        # if we want to get a comment, use the serializer to return the comment
        return Response(serializer.data)
    
# TODO: add the ability to PATCH comments

@api_view(['GET', 'POST', 'DELETE'])
def like_post(request, pk):
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