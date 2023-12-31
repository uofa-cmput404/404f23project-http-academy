from django.shortcuts import render
from .models import Post, Comment, Like
from django.urls import reverse
from .serializers import PostSerializer, CommentSerializer, CommentLikeSerializer
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
from drf_yasg.utils import swagger_auto_schema
from node.node_functions import send_post_toInbox, fetchRemotePosts, testsend_post_to_remoteInbox, sendComment_toRemoteHost
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

def get_user(pk):
    try:
        user = AppUser.objects.get(pk=pk)
    except AppUser.DoesNotExist:
        return None
    return user


def get_object(user, post_id):
    try:
        return user.post_user.get(post_id=post_id)
    except Post.DoesNotExist:
        return None


@api_view(['GET'])
def own_posts_list(request, pk):
    user_id = pk
    try:
        user = get_user(pk)
        if user:
            # Fetch the user's own posts without order_by
            posts = Post.objects.filter(author=user)

            # Identify friends as those who are both followers and following
            # followers = set(user.followers.all())
            # following = set(user.following.all())
            # friends = followers.intersection(following)

            # Fetch friends' private and friends-only posts without order_by
            # friends_posts = Post.objects.filter(
            #     author__in=friends,
            #     visibility__in=["PRIVATE", "FRIENDS_ONLY"]
            # )

            # Combine user's own posts with friends' posts and then apply order_by
            # posts = own_posts.union(friends_posts).order_by('-published')
            print('all posts on profile', posts)
        else:
            # Fetch all public posts
            posts = Post.objects.filter(
                visibility="PUBLIC").order_by('-published')

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
        return Response({"type": "posts", "items": serializer.data}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        raise NotFound(detail="Author not found", code=404)


@api_view(['GET', 'POST'])
def posts_list(request, pk=None):
    if request.method == 'POST':
        all_users = AppUser.objects.all()
        matched_user = None

        filtered = all_users.filter(foreign__contains=request.data["author"])

        if filtered.count() > 0:
            for user in all_users:
                print("User url", user.url)
                if str(user.foreign) == request.data["author"]:
                    matched_user = user
            request.data["author"] = str(matched_user.user_id)

        print('request data', request.data)
        # if we want to create a new post, use the serializer and save if valid
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            # serializer.save()
            # post_created = serializer.data
            # user = get_user(pk)
            # testsend_post_to_remoteInbox(post_created, user)
            post = serializer.save()  # Save and get the post instance
            if pk:
                user = get_user(pk) 
                print('post object', post.image_url)
                testsend_post_to_remoteInbox(post, user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('serializer eroorrs', serializer)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # fetchRemotePosts()

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
            # print('data returned to front end', serializer.data)
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
def comments_list(request, pk, post_id):
    if request.method == 'POST':
        # print('Received comment data:', request.data)
        # print('Comment post ID:', type(post_id))

        request_data_with_postId = request.data.copy()
        request_data_with_postId['postId'] = post_id
        user = get_object_or_404(AppUser, pk=pk)
        serializer = CommentSerializer(data=request_data_with_postId)
        if serializer.is_valid():

            print('it actually worked and saved a comment')
            serializer.save()
            comment_toSend = serializer.data

            print('comment to send', comment_toSend["id"])
            sendComment_toRemoteHost(comment_toSend, user)
        else:
            print('serialzier eerror', serializer.errors)
            return Response(serializer.errors)
    else:
        # Handling GET request
        print('post id for comment', post_id)
        print(' ig tohere to retrieve data', Comment.objects.all())
        comments = Comment.objects.filter(postId=post_id)
        print('cmment for my post', comments)
        serializer = CommentSerializer(comments, many=True)
        print('ser data', serializer.data)
        return Response(serializer.data)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
def comment_like(request, pk, comment_id):
    try:
        author = AppUser.objects.get(pk=pk)
        authorid = author.user_id
        comment = Comment.objects.get(pk=comment_id)
    except (AppUser.DoesNotExist, Comment.DoesNotExist):
        return Response({"error": "Comment or Author not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        likes = Like.objects.filter(commentId=comment.comment_id)
        serializer = CommentLikeSerializer(likes, many=True)
        response_data = serializer.data
        print('response backkk', response_data)
        # Add the authorid to the response data
        # response_data['authorid'] = authorid
        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        user_id = request.data.get('author')
        user = get_object_or_404(AppUser, pk=user_id)

        # Check if the user already liked this comment
        if Like.objects.filter(author=user, commentId=comment).exists():
            return Response({"error": "You have already liked this comment"}, status=status.HTTP_400_BAD_REQUEST)

        print('new like is genearted')
        new_like = Like(author=user, commentId=comment)
        new_like.save()
        return Response({"message": "Comment liked successfully"}, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        print('i got here to unlike a commen', comment_id, pk)
        # user_id = request.data.get('author')
        user = get_object_or_404(AppUser, pk=pk)

        # Find the like to delete
        like = Like.objects.filter(author=user, commentId=comment)
        if like.exists():
            like.delete()
            return Response({"message": "Like removed successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET', 'DELETE', 'PATCH'])
def comment_detail(request, pk, post_id):
    # get the comment with the specified ID
    comment = Comment.objects.get(id=post_id)
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


@api_view(['GET'])
@swagger_auto_schema(operation_description="Get all image data for a post", responses={200: "{'type': 'author', 'id': {id}}", 400: "{'type': 'error', 'message': {errors}}"})
def get_post_image(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data["image"])

@api_view(['GET'])
def search_posts(request, query):
    # TODO: Handle the error when nothing is found
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query))
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def homepage(request, pk):
    try:
        user = get_user(pk)
        followers = set(user.followers.all())
        following = set(user.following.all())
        friends = followers.intersection(following)
        friends_posts = Post.objects.filter(
            author__in = friends,
            visibility__in = ["PRIVATE", "FRIENDS_ONLY"]
        )
        user_private_and_friends_posts = Post.objects.filter(
            author = user,
            visibility__in = ["PRIVATE", "FRIENDS_ONLY"]
        )
        public_posts = Post.objects.filter(visibility="PUBLIC")
        posts = public_posts.union(friends_posts)
        posts = posts.union(user_private_and_friends_posts)

        posts = posts.order_by('-published')
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
        # print('data returned to front end', serializer.data)
        return Response({"type": "homepage", "items": serializer.data}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        raise NotFound(detail="Author not found", code=404)