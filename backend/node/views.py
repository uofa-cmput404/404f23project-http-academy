from .models import Node
from .serializers import NodeSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import base64
import requests





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



@api_view(['GET'])
def getNodePosts(request):

    allPosts = []

    for node in Node.objects.all(): 
        # get the host from header
        remoteHost = node.host
        if remoteHost == None: # this will not work for error checking - need to use raise valueError
            response = {"error":"Please provide a valid hostname or IP address"}
            return Response(response, status.HTTP_200_OK)

        # get each author from the remote host
        try:
            AuthorRequest = requests.request.get(f'http://{remoteHost}/authors/',auth={node.username, node.password})
        except Exception as e:
            print(f"failed to get authors from {remoteHost}")
            
        if AuthorRequest.status_code != 200:
            response = {"error": "Couldn't connect to the specified server"}
            return Response(response, status.HTTP_200_OK)
        else:
            remoteAuthors = AuthorRequest.json().get('items')
            for author in remoteAuthors:
                # for every author, get their posts from remote
                try:
                    remoteAuthorPostsRequest = requests.request.get(f"{author['id']}/posts/",auth={node.username, node.password})
                except Exception as e:
                    print(f"failed to get posts from author {author['id']}")
                
                if remoteAuthorPostsRequest.status_code != 200:
                    response = {"error": "Couldn't connect to the specified server"}
                    return Response(response, status.HTTP_200_OK)
                else:
                    remoteAuthorPosts = remoteAuthorPostsRequest.json().get('items')
                    allPosts.extend(remoteAuthorPosts)

    response = {
        "type": "posts",
        "items":allPosts
    }
    return Response(response, status.HTTP_200_OK)


@api_view(['GET'])
def getRemoteAuthors(request):
    allAuthors = []
    
    for node in Node.objects.all(): 
        # get the host from header
        remoteHost = node.host
        if remoteHost == None: # this will not work for error checking - need to use raise valueError
            response = {"error":"Please provide a valid hostname or IP address"}
            return Response(response, status.HTTP_200_OK)

        # get each author from the remote host
        try:
            AuthorRequest = requests.request.get(f'http://{remoteHost}/authors/',auth={node.username, node.password})
        except Exception as e:
            print(f"failed to get authors from {remoteHost}")
            
        if AuthorRequest.status_code != 200:
            response = {"error": "Couldn't connect to the specified server"}
            return Response(response, status.HTTP_200_OK)
        else:
            remoteAuthors = AuthorRequest.json().get('items')
            allAuthors.extend(remoteAuthors)

    response = {
        "type": "authors",
        "items":allAuthors
    }
    return Response(response, status=status.HTTP_200_OK)