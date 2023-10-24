from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
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