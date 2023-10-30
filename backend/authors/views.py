from django.shortcuts import render
from .models import author
from .serializers import AuthorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status




@api_view(['GET', 'POST'])
def authors_list(request):
    if request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Use status from rest_framework
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Use status from rest_framework
    else:
        authors = author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  # Use status from rest_framework
    

@api_view(['GET', 'DELETE'])
def authors_detail(request, pk):
    authors = author.objects.get(user_id=pk)
    serializer = AuthorSerializer(authors, many=False)

    if request.method == 'DELETE':
        try:
            authors.delete()
            return Response('Author deleted successfully')
        except:
            return Response('Author does not exist')
    else:
        return Response(serializer.data)