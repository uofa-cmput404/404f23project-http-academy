
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from authors.models import AppUser
from posts.models import Post

from .models import Like
from .serializers import LikeSerializer

class LikesView(APIView):
    def get(self, request: Request, pk: str, post_id: str, comment_id:str = None) -> Response:
        """Return the likes of the post."""
        if comment_id is None:
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                raise Http404("Post does not exist")


            likes = list(Like.objects.filter(object=post.url))
            likes = LikeSerializer(likes, many=True)
            likes_dict = {"type": "likes", "items": likes.data}
            return Response(likes_dict, status=status.HTTP_200_OK)

       

    def post(self, request: Request, pk: str, post_id: str) -> Response:
        """Add a like to the post."""
        liking_author = get_object_or_404(AppUser, pk=pk)  # The user who likes the post
        post_to_like = get_object_or_404(Post, pk=post_id)  # The post being liked

        print('liing author', liking_author, post_to_like)
        if Like.objects.filter(author=liking_author, object=post_to_like.url).exists():
            return Response({"error": "Post already liked by this author"}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(author=liking_author, object=post_to_like.url, summary=f"{liking_author.displayName} likes {post_to_like.title}.")
        return Response({"type": "Like", "detail": f"{liking_author.displayName} liked {post_to_like.url}."}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, post_id):
        author = get_object_or_404(AppUser, pk=pk)
        post = get_object_or_404(Post, pk=post_id)

        like = Like.objects.filter(author=author, object=post.url)
        if like.exists():
            like.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Like not found."}, status=status.HTTP_404_NOT_FOUND)
    

class LikedView(APIView):
    
    def get(self, request, author_id):
        """Return the posts that the author liked."""
        author = get_object_or_404(AppUser, pk=author_id)
        liked = Like.objects.filter(author=author)
        liked_serializer = LikeSerializer(liked, many=True)

        return Response({
            "type": "liked",
            "items": liked_serializer.data
        }, status=status.HTTP_200_OK)