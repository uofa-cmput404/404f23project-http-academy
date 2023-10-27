from django.shortcuts import render
from .models import authors
from .serializers import AuthorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def authors_list(request):
    if request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
    else:
        authors = AuthorSerializer.objects.all()
        serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def authors_detail(request, pk):
    post = authors.objects.get(id=pk)
    serializer = AuthorSerializer(post, many=False)

    if request.method == 'DELETE':
        try:
            post.delete()
            return Response('Post deleted successfully')
        except:
            return Response('Post does not exist')
    else:
        return Response(serializer.data)