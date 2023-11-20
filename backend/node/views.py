from posts.serializers import PostSerializer
from posts.models import Post
# from node.utils import authenticated_GET, our_hosts


from rest_framework.generics import GenericAPIView
from .models import Node
# from .serializers import NodeSerialize


from rest_framework.decorators import api_view, permission_classes
from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
import requests
import base64


# from backend.utils import is_our_frontend
from operator import itemgetter


credentialForConnect = {"username" : "hello", "password" : "world"}  # credential to connect
credentialForDelete = {"", "", "", ""}

