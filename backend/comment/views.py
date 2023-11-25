# from django.shortcuts import get_object_or_404
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.exceptions import ValidationError
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Comment, AppUser, Post
# from .serializers import CommentSerializer

# class CommentDetail(APIView):

#     def get_object(self, model, **kwargs):
#         return get_object_or_404(model, **kwargs)

#     def paginate_queryset(self, queryset, request):
#         paginator = PageNumberPagination()
#         paginator.page_size = request.query_params.get('size', 5)
#         return paginator.paginate_queryset(queryset, request)

#     def get(self, request, pk, post_id, comment_id=None):
#         author = self.get_object(AppUser, pk=pk)
#         post = self.get_object(Post, post_id=post_id, author=author)

#         if comment_id:
#             comment = self.get_object(Comment, comment_id=comment_id, post=post)
#             serializer = CommentSerializer(comment)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             comments = post.post_comment.all()
#             paginated_comments = self.paginate_queryset(comments, request)

#             if paginated_comments is not None:
#                 serializer = CommentSerializer(paginated_comments, many=True)
#                 return Response({
#                     "type": "comments",
#                     "page": request.query_params.get("page", 1),
#                     "size": len(serializer.data),
#                     "post": str(post.url),
#                     "comments": serializer.data
#                 }, status=status.HTTP_200_OK)
#             else:
#                 serializer = CommentSerializer(comments, many=True)
#                 return Response({
#                     "type": "comments",
#                     "page": 1,
#                     "size": len(serializer.data),
#                     "post": str(post.url),
#                     "comments": serializer.data
#                 }, status=status.HTTP_200_OK)

#     def post(self, request, pk, post_id):
#         author = self.get_object(AppUser, pk=pk)
#         post = self.get_object(Post, post_id=post_id, author=author)

#         comment_data = request.data.copy()
#         comment_data['post'] = post.id
#         comment_data['author'] = author.id

#         serializer = CommentSerializer(data=comment_data)
#         if serializer.is_valid():
#             comment = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             raise ValidationError(serializer.errors)

