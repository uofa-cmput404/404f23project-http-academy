from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from rest_framework.response import Response
from .models import AppUser, Follower, FollowRequest
from .serializers import UserUpdateSerializer


class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				user_data = {
				"id": user.user_id,
				"email": user.email,
				"username": user.username
				}
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			print('this is the returned response to client', user.user_id, user.email, user.password)
			user_data = {
				"id": user.user_id,
				"email": user.email,
				"username": user.username
			}
			return Response(user_data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserUpdate(APIView):
    permission_classes = (permissions.IsAuthenticated,)		
    def get_object(self, pk):
        try:
            return AppUser.objects.get(pk=pk)
        except AppUser.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

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
	
	def get(self, request):
		serializer = UserSerializer(AppUser.objects.all(), many=True)
		authors = AppUser.objects.all()
		authors_data = []
		
		for author in authors:
			author_data = {
				"type": "author",
				"id": request.build_absolute_uri(author.get_absolute_url()),  # Assuming you have implemented get_absolute_url method in the Author model
				"url": request.build_absolute_uri(author.get_absolute_url()),
				"host": request.build_absolute_uri('/'),
				"displayName": author.username,
				"github": author.github,
				"profileImage": author.profileImage
			}
			authors_data.append(author_data)

		response = {
			'type' : 'authors', #harcoded, needs to change
			'items': authors_data,
		}
		
		return Response(response, status=status.HTTP_200_OK)
		# customize it beofre sending
		

class UserDetails(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	
	def get(self, request, pk):
		try:
			author = AppUser.objects.get(pk=pk)
		except AppUser.DoesNotExist:
			return Response({"status": 1,
						"message": "Part not found"}, status=status.HTTP_404_NOT_FOUND)
		serializer = UserSerializer(author)
		return Response(serializer.data, status=status.HTTP_200_OK)
	

class FollowerList(APIView):

	def get(self, request, pk):
		# get all followers of a given author id
		items =[]
		for follower in Follower.objects.filter(author=pk):
			try:
				author = AppUser.objects.get(pk=follower.follower.user_id)
			except AppUser.DoesNotExist:
				continue
			author_data = {
				"type": "author",
				"id": request.build_absolute_uri(author.get_absolute_url()),
				"url": request.build_absolute_uri(author.get_absolute_url()),
				"host": request.build_absolute_uri('/'),
				"displayName": author.username,
				"github": author.github,
				"profileImage": author.profileImage
			}
			items.append(author_data)
		response = {
			"type": "followers",
			"items": items,
		}

		return Response(response, status=status.HTTP_200_OK)


class FollowerDetail(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, pk, follower_id):
		is_following = False
		# check if the user with follower_id is following the user with pk
		if Follower.objects.filter(author=pk, follower=follower_id).exists():
			is_following = True
		response = {
			"type": "followers",
			"is_following": is_following,
		}

		return Response(response, status=status.HTTP_200_OK)
	
	def put(self, pk, follower_id):
		# check if the user with follower_id is following the user with pk
		if Follower.objects.filter(author=pk, follower=follower_id).exists():
			return Response({
				"type": "followers",
				"message": "following"}, status=status.HTTP_400_BAD_REQUEST)
		
		# add the user with follower_id to the followers of the user with pk
		try:
			follower = AppUser.objects.get(pk=follower_id)
			author = AppUser.objects.get(pk=pk)
			follower_obj = Follower.objects.create(author=author, follower=follower)
			follower_obj.save()
		except AppUser.DoesNotExist:
			# if either userID specified is not found, return 404
			return Response({
				"type": "followers",
				"message": "follower not found"}, status=status.HTTP_404_NOT_FOUND)
		
		return Response({
			"type": "followers",
			"message": "follower added"}, status=status.HTTP_200_OK)
	
	def delete(self, pk, follower_id):
		# check if the user with follower_id is following the user with pk
		if Follower.objects.filter(author=pk, follower=follower_id).exists():
			# delete the user with follower_id from the followers of the user with pk
			Follower.objects.filter(author=pk, follower=follower_id).delete()
			return Response({
				"type": "followers",
				"message": "follower deleted"}, status=status.HTTP_200_OK)
		else:
			return Response({
				"type": "followers",
				"message": "follower not found"}, status=status.HTTP_404_NOT_FOUND)


class FollowRequestDetail(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, request, pk, object_author):
		# return follow request from a given author (object_author) to a given author (pk)
		# TODO: this isn't working; apparently FollowRequest has no attribute 'object'
		followRequest = FollowRequest.objects.filter(object=object_author, actor=pk)
		if followRequest is None:
			return Response({
				"type": "follow",
				"message": "follow request not found"}, status=status.HTTP_404_NOT_FOUND)

		try:
			# get the author objects for both authors in the follow request
			follower = AppUser.objects.get(pk=pk)
			author = AppUser.objects.get(pk=object_author)
		except AppUser.DoesNotExist:
			return Response({
				"type": "follow",
				"message": "author not found"}, status=status.HTTP_404_NOT_FOUND)
		
		actor = {
			"type": "author",
			"id": request.build_absolute_uri(follower.get_absolute_url()),
			"url": request.build_absolute_uri(follower.get_absolute_url()),
			"host": request.build_absolute_uri('/'),
			"displayName": follower.username,
			"github": follower.github,
			"profileImage": follower.profileImage
		}

		obj = {
			"type": "author",
			"id": request.build_absolute_uri(author.get_absolute_url()),
			"url": request.build_absolute_uri(author.get_absolute_url()),
			"host": request.build_absolute_uri('/'),
			"displayName": author.username,
			"github": author.github,
			"profileImage": author.profileImage
		}

		response = {
			"type": "follow",
			"summary": "{} wants to follow {}".format(follower.username, author.username),
			"actor": actor,
			"object": obj,
		}

		return Response(response, status=status.HTTP_200_OK)
	
	def put(self, request, pk, object_author):
		# create a follow request from a given author (object_author) to a given author (pk)
		followRequest = FollowRequest.objects.filter(author=object_author, follower=pk)
		if followRequest is not None:
			return Response({
				"type": "follow",
				"message": "follow request already exists"}, status=status.HTTP_400_BAD_REQUEST)
		# check if the user with follower_id is already following the user with pk
		if Follower.objects.filter(author=object_author, follower=pk) is not None:
			return Response({
				"type": "follow",
				"message": "already following"}, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			# get the author objects for both authors in the follow request
			follower = AppUser.objects.get(pk=pk)
			author = AppUser.objects.get(pk=object_author)
		except AppUser.DoesNotExist:
			return Response({
				"type": "follow",
				"message": "author not found"}, status=status.HTTP_404_NOT_FOUND)
		
		follow_request_obj = FollowRequest.objects.create(author=author, follower=follower)
		follow_request_obj.save()

		return Response({
			"type": "follow",
			"message": "follow request created"}, status=status.HTTP_200_OK)