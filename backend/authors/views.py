
# from django.contrib.auth import get_user_model, login, logout
# from rest_framework.authentication import SessionAuthentication
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
# from rest_framework import permissions, status
# from .validations import custom_validation, validate_email, validate_password
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import AppUser
# from .serializers import UserUpdateSerializer
# from inbox.models import Inbox
# from django.middleware.csrf import get_token
# # Create your views here.


# from rest_framework import generics
# class UserRegister(APIView):
# 	permission_classes = (permissions.AllowAny,)
# 	def post(self, request):
# 		clean_data = custom_validation(request.data)
# 		serializer = UserRegisterSerializer(data=clean_data)
# 		if serializer.is_valid(raise_exception=True):
# 			user = serializer.create(clean_data)
# 			Inbox.objects.create(authorId=user)
# 			print()
# 			if user:
# 				user_data = {
# 				"id": user.user_id,
# 				"email": user.email,
# 				"username": user.username,
# 				"displayName": user.username
# 				}
# 				return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(status=status.HTTP_400_BAD_REQUEST)


# class UserLogin(APIView):
# 	permission_classes = (permissions.AllowAny,)
# 	authentication_classes = (SessionAuthentication,)
# 	##
# 	def post(self, request):
# 		data = request.data
# 		assert validate_email(data)
# 		assert validate_password(data)
# 		serializer = UserLoginSerializer(data=data)
# 		if serializer.is_valid(raise_exception=True):
# 			user = serializer.check_user(data)
# 			login(request, user)
# 			serializer = UserSerializer(user)
# 			csrf_token = get_token(request)
# 			print('hit this ogo', csrf_token)
# 			response = {"user": serializer.data, "csrf_token": csrf_token}
# 			print('response sent back to the front end', response)
# 			return Response(response, status=status.HTTP_200_OK, headers = {'X-Csrftoken': csrf_token})

# class UserLogout(APIView):
# 	permission_classes = (permissions.AllowAny,)
# 	authentication_classes = ()
# 	def post(self, request):
# 		logout(request)
# 		return Response(status=status.HTTP_200_OK)


# class UserUpdate(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
# 	# authentication_classes = (SessionAuthentication,)
#     def get_object(self, pk):
#         try:
#             return AppUser.objects.get(pk=pk)
#         except AppUser.DoesNotExist:
#             raise Http404

#     def patch(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = UserUpdateSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserView(APIView):
# 	permission_classes = (permissions.IsAuthenticated,)
# 	authentication_classes = (SessionAuthentication,)

# 	def get(self, request):
# 		serializer = UserSerializer(AppUser.objects.all(), many=True)
# 		authors = AppUser.objects.all()
# 		authors_data = []

# 		for author in authors:
# 			author_data = {
# 				"type": "author",
# 				"id": request.build_absolute_uri(author.get_absolute_url()),  # Assuming you have implemented get_absolute_url method in the Author model
# 				"url": request.build_absolute_uri(author.get_absolute_url()),
# 				"host": request.build_absolute_uri('/'),
# 				"displayName": author.username,
# 				"github": author.github,
# 				"profileImage": author.profileImage
# 			}
# 			authors_data.append(author_data)

# 		response = {
# 			'type' : 'authors', #harcoded, needs to change
# 			'items': authors_data,
# 		}

# 		return Response(response, status=status.HTTP_200_OK)
# 		# customize it beofre sending


# class UserDetails(APIView):
# 	permission_classes = (permissions.IsAuthenticated,)
# 	authentication_classes = (SessionAuthentication,)

# 	def get(self, request, pk):
# 		try:
# 			author = AppUser.objects.get(pk=pk)
# 		except AppUser.DoesNotExist:
# 			return Response({"status": 1,
# 						"message": "Part not found"}, status=HTTP_404_NOT_FOUND)
# 		serializer = UserSerializer(author)

# 		return Response(serializer.data, status=status.HTTP_200_OK)
# from django.shortcuts import render
# from .models import Author
# from .serializers import AuthorSerializer
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# # Create your views here.
# @api_view(['GET', 'POST'])
# def author_list(request):
#     if request.method == 'POST':
#         # if we want to create a new author
#         serializer = AuthorSerializer(data=request.data)
#         if serializer.is_valid():
#             print('here')
#             serializer.save()
#         else:
#             return Response(serializer.errors)
#     else:
#         # get all authors
#         authors = Author.objects.all()
#         serializer = AuthorSerializer(authors, many=True)
#     return Response(serializer.data)
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AppUser
from .serializers import UserUpdateSerializer
from inbox.models import Inbox
from django.middleware.csrf import get_token
# from node import getNodePosts
# Create your views here.

from drf_yasg.utils import swagger_auto_schema
from node.node_functions import fetchRemoteAuthors, fetchRemotePosts, send_remoteUser

from rest_framework import generics


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(operation_description="Register a user", request_body=UserRegisterSerializer, responses={201: "{'type': 'author', 'id': {id}}", 400: "{'type': 'error', 'message': {errors}}"})
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            send_remoteUser(user)
            Inbox.objects.create(authorId=user)
            print()
            if user:
                user_data = {
                    "id": user.user_id,
                    "email": user.email,
                    "username": user.username,
                    "displayName": user.username
                }
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    ##

    @swagger_auto_schema(operation_description="Login a user", request_body=UserLoginSerializer, responses={200: "{'type': 'author', 'id': {id}}", 400: "{'type': 'error', 'message': {errors}}"})
    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            serializer = UserSerializer(user)
            csrf_token = get_token(request)
            # print('hit this ogo', csrf_token)
            response = {"user": serializer.data, "csrf_token": csrf_token}
            # print('response sent back to the front end', response)

            return Response(response, status=status.HTTP_200_OK, headers={'X-Csrftoken': csrf_token})


class UserLogout(APIView):

    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    @swagger_auto_schema(operation_description="Logout a user", responses={200: "{'type': 'author', 'id': {id}}", 400: "{'type': 'error', 'message': {errors}}"})
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserUpdate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (SessionAuthentication,)

    def get_object(self, pk):
        try:
            return AppUser.objects.get(pk=pk)
        except AppUser.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description="Update a specific author", request_body=UserSerializer, responses={200: "{'type': 'author', 'id': {id}}", 400: "{'type': 'error', 'message': {errors}}"})
    def patch(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    # maybe we do this when the user logs in - liek retrive al lthe data and put in a store
    # for perfomance reasons so we dont have to calling the remote end points everytime the user
    # navigates to the hub

    @swagger_auto_schema(operation_description="Get a list of all authors", responses={200: UserSerializer(many=True), 400: 'Bad Request'})
    def get(self, request):
        # print('triggered')
        serializer = UserSerializer(AppUser.objects.all(), many=True)
        # remote_authors = fetchRemoteAuthors()
        # print('remotinng', remote_authors)
        # call the function in node
        authors = AppUser.objects.all()
        authors_data = []

        for author in authors:
            author_data = {
                "type": "author",
                # Assuming you have implemented get_absolute_url method in the Author model
                "id": request.build_absolute_uri(author.get_absolute_url()),
                "url": request.build_absolute_uri(author.get_absolute_url()),
                "host": request.build_absolute_uri('/'),
                "displayName": author.username,
                "github": author.github,
                "profileImage": author.profileImage
            }
            authors_data.append(author_data)

        response = {
            'type': 'authors',  # harcoded, needs to change
            'items': authors_data,
        }

        return Response(response, status=status.HTTP_200_OK)
        # customize it beofre sending


class UserDetails(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    @swagger_auto_schema(operation_description="Get a specific author", responses={200: UserSerializer, 400: 'Bad Request'})
    def get(self, request, pk):
        try:
            author = AppUser.objects.get(pk=pk)
        except AppUser.DoesNotExist:
            return Response({"status": 1,
                             "message": "Part not found"}, status=HTTP_404_NOT_FOUND)
        serializer = UserSerializer(author)

        return Response(serializer.data, status=status.HTTP_200_OK)