from django.shortcuts import render
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET', 'POST'])
def posts_list(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
    else:
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)

    if request.method == 'DELETE':
        try:
            post.delete()
            return Response('Post deleted successfully')
        except:
            return Response('Post does not exist')
    else:
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def comments_list(request, pk):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
    else:
        comments = Comment.objects.filter(postId=pk)
        serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def comment_detail(request, pk):
    comment = Comment.objects.get(id=pk)
    serializer = CommentSerializer(comment, many=False)

    if request.method == 'DELETE':
        try:
            comment.delete()
            return Response('Comment deleted successfully')
        except:
            return Response('Comment does not exist')
    else:
        return Response(serializer.data)
    
@api_view(['GET', 'POST', 'DELETE'])
def like_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        try:
            post.likes += 1
            post.save()
            return Response('Post liked successfully')
        except:
            return Response('Post does not exist')
    elif request.method == 'DELETE':
        try:
            post.likes -= 1
            post.save()
            return Response('Post unliked successfully')
        except:
            return Response('Post does not exist')
    else:
        likes = post.likes
        return Response(likes)