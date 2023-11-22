from django.shortcuts import render
from .models import Post, Comment, Like
from django.urls import reverse 
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from authors.models import AppUser
import uuid 
from django.http import Http404
from django.shortcuts import get_object_or_404


def get_user(pk):
        try:
            user = AppUser.objects.get(pk=pk)
        except AppUser.DoesNotExist:
            return None
        return user

def get_object(user,post_id):
        try:
            return user.post_user.get(post_id=post_id)
        except Post.DoesNotExist:
            return None

@api_view(['GET'])
def own_posts_list(request, pk):
    user_id = pk
    try:
        # Filter posts based on user_id if provided
        user = get_user(pk)
        if user:
           
            print('user_id', user_id)
            print('type of user_id', type(user_id))
            # Fetch posts for the specific author
            posts = Post.objects.filter(author__user_id=user_id).order_by('-published')
            print('i got here in the new own posts', posts)
        else:
            # Fetch all public posts
            posts = Post.objects.filter(visibility="PUBLIC").order_by('-published')

        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)
        paginator = Paginator(posts, size)

        try:
            posttosee = paginator.page(page)
        except PageNotAnInteger:
            posttosee = paginator.page(1)
        except EmptyPage:
            posttosee = paginator.page(paginator.num_pages)

        serializer = PostSerializer(posttosee, many=True)
        return Response({"type": "publicposts", "items": serializer.data}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        raise NotFound(detail="Author not found", code=404)
    



@api_view(['GET', 'POST'])
def posts_list(request, pk = None):
    if request.method == 'POST':
        # if we want to create a new post, use the serializer and save if valid
        serializer = PostSerializer(data=request.data)
      
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        print('got here to get post')
        try:
            
            if pk:
                # Fetch posts for a specific author
                posts = Post.objects.filter(author__user_id=pk)
                
                if request.user.is_authenticated and request.user.user_id == pk:
                    # If the request user is the author, show all their posts
                    posts = posts
                    print('here are my posts', posts)
                else:
                    # Otherwise, show only public posts of the author
                    posts = posts.filter(visibility="PUBLIC")

            else:
                # Fetch all public posts if no author id is provided
                posts = Post.objects.filter(visibility="PUBLIC")

            posts = posts.order_by('-published')
            print('published posts', posts)
            page = request.query_params.get('page', 1)
            size = request.query_params.get('size', 10)
            paginator = Paginator(posts, size)

            try:
                posttosee = paginator.page(page)
            except PageNotAnInteger:
                posttosee = paginator.page(1)
            except EmptyPage:
                posttosee = paginator.page(paginator.num_pages)

            serializer = PostSerializer(posttosee, many=True)
            print('data returned to front end', serializer.data)
            return Response({"type": "publicposts", "items": serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            
            raise NotFound(detail="Author not found", code=404)



@api_view(['GET', 'DELETE', 'PATCH'])
def post_detail(request, pk, post_id):

    author = get_object_or_404(AppUser, pk=pk)
    # Get the post with the specified ID
    post = get_object_or_404(Post, author=author, post_id=post_id)

    if request.method == 'DELETE':
        try:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            
            return Response({"error": "Deletion failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'PATCH':
        # Check for fields that should not be updated
        # print('i got this data to update', request.data)
        if any(field in request.data for field in ['id', 'author', 'published', 'count', 'likes']):
            return Response({"error": "Cannot update certain fields"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # print('serializer eroorrs', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:  #
        serializer = PostSerializer(post)
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
    
# @api_view(['GET', 'POST'])
# def like_post(request, pk):
    
#     likes = Like.objects.filter(postId=pk)
#     print("these are the likes:  ")
#     print(likes)
#     already_liked = len(likes.filter(author=request.data.get('author'))) > 0
#     print(already_liked)
#     if request.method == 'POST':
#         # if we want to create a new like, use the serializer and save if valid
#         serializer = PostLikeSerializer(data=request.data)
#         print("is valid: " + str(serializer.is_valid()))
#         if serializer.is_valid() and not already_liked:
#             serializer.save()
#         else:
#             return Response(serializer.errors)
#     else:
#         # if we want to get all likes for a post, use the serializer to return all likes
#         serializer = PostLikeSerializer(likes, many=True)
#         likes = Like.objects.filter(postId=pk)
#     return Response(serializer.data)
    

# '''
#     # get the post with the specified ID
#     post = Post.objects.get(id=pk)
#     if request.method == 'POST':
#         # if we're liking a post, increment the likes and save if valid
#         try:
#             post.likes += 1
#             post.save()
#             return Response('Post liked successfully')
#         except:
#             return Response('Post does not exist')
#     elif request.method == 'DELETE':
#         # if we're unliking a post, decrement the likes and save if valid
#         try:
#             post.likes -= 1
#             post.save()
#             return Response('Post unliked successfully')
#         except:
#             return Response('Post does not exist')
#     else:
#         # if we want to get the number of likes for a post, return the number of likes
#         likes = post.likes
#         return Response(likes)
# '''

# @api_view(['GET', 'DELETE'])
# def like_detail(request, pk, pkLike):
#     # get the like with the specified ID
#     like = Like.objects.get(postId=pk , id = pkLike)
#     serializer = PostLikeSerializer(like, many=False)

#     if request.method == 'DELETE':
#         # if we want to delete a like, delete it and return a success message if it exists
#         try:
#             like.delete()
#             return Response('Like deleted successfully')
#         except:
#             return Response('Like does not exist')
#     else:
#         # if we want to get a like, use the serializer to return the like
#         return Response(serializer.data)



@api_view(['GET'])
def get_post_image(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data["image"])