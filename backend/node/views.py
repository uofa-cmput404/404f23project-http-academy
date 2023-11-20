from .models import Node
from .serializers import NodeSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import base64





credentialForConnect = {"username" : "hello", "password" : "world"}  # credential to connect
credentialForDelete = {"", "", "", ""}

@api_view(['POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def authRemoteNode(request, host):

    # check if basic authorization is provided and valid
    if (request.META.get('HTTP_AUTHORIZATION') != None and
         'Basic' in request.META.get('HTTP_AUTHORIZATION')):
        
        # get the encoded user and pass
        auth_header = request.META['HTTP_AUTHORIZATION']
        username, password = base64.b64decode(auth_header[6:]).split(":")

        # check credentials to make sure they are able to connect
        if username == credentialForConnect["username"] and password == credentialForConnect["password"]:
            
            # create new node object
            remoteNode = Node(host=host, username=host, password=host)
            remoteNode.save()

            # return ok
            response = {
                "username":remoteNode.username,
                "password":remoteNode.password
            }  
            return Response(response, status.HTTP_200_OK)

        # otherwise error for bad basic auth credentials
        response = {"message":"Incorrect Credentials"}        
        return Response(response, status.HTTP_400_BAD_REQUEST)

    else:
        # otherwise bad connection
        response = {"message":"Invalid Basic Auth"}        
        return Response(response, status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def getNode(request):

    # get the host from header
    remoteHost = request.GET.get("host")

    if remoteHost:
        try:
            # find the node with that hostname
            nodes = Node.objects.get(host=remoteHost)
            serializer = NodeSerializer(nodes)

            # if node does not exist send error
            if Node.DoesNotExist:
                response = {"error":"No such node exists"}
                return Response(response, status.HTTP_200_OK)
            else:
                response = serializer.data
                return Response(response, status.HTTP_200_OK)
            
        except:
            response = {"error":"Error occurred while fetching data from the database."}
            return Response(response, status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        response = {"error":"Please provide a valid hostname or IP address"}
        return Response(response, status.HTTP_400_BAD_REQUEST)

