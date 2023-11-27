from .models import Node
from .serializers import NodeSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import base64
import requests
from authors.models import AppUser
from followers.models import FriendRequest
from followers.serializers import FriendRequestSerializer
from posts.models import Post 
from inbox.models import Inbox
from posts.serializers import PostSerializer
import json 
LOCALHOSTS = ["http://127.0.0.1/", "https://cmput404-httpacademy2-1c641b528836.herokuapp.com/",
                    "http://127.0.0.1:8000/"]

def fetchRemoteAuthors():
    allAuthors = []
    node = Node.objects.first()
 
    if node:
        remoteHost = node.host
        if not remoteHost:
            return allAuthors

        request_url = f'{remoteHost}service/authors/'
        # print('request url', request_url) 
        try:
            response = requests.get(request_url, auth=(node.username, node.password))
            if response.status_code == 200:
                remoteAuthors = response.json().get('items', [])
                print('remote authors', json.dumps(response.json(), indent = 4))
                for raw_author in remoteAuthors:
                    transformed_author = transform_author_data(raw_author, node.team)
                    # print('remote author', transformed_author)
                    
                    # Update or create the author in the database
                    create_or_update_author(transformed_author)
                    allAuthors.append(transformed_author)

                    
        except requests.exceptions.RequestException as e:
            print(f"Error fetching authors from {remoteHost}: {e}")
            return allAuthors

    return allAuthors


def fetchRemotePosts():
    allPosts = []
    nodes = Node.objects.all()

    if len(nodes) > 1:  # Make sure there is at least a second node
        node = nodes[1]  # Get the second node

        remoteHost = node.host
        if not remoteHost:
            return allPosts
        request_url = f'{remoteHost}api/posts/'
        print('request url', request_url)
        # print('request url', request_url) 
        # try:
        #     response = requests.get(request_url, auth=(node.username, node.password))
        #     print('response from other team 2', json.dumps(response.json()))
        #     if response.status_code == 200:
        #         remoteAuthors = response.json().get('items', [])
        #         # print('remote posts', json.dumps(response.json(), indent = 4))
        #         # for raw_author in remoteAuthors:
        #         #     transformed_author = transform_author_data(raw_author, node.team)
        #         #     # print('remote author', transformed_author)
                    
        #         #     # Update or create the author in the database
        #         #     create_or_update_author(transformed_author)
        #         #     allAuthors.append(transformed_author)

                    
        # except requests.exceptions.RequestException as e:
        #     print(f"Error fetching authors from {remoteHost}: {e}")
        #     return allPosts

    return allPosts


def create_or_update_author(author_data):
    """
    Create or update an author in the database.
    :param author_data: The transformed author data.
    """
    user_id = author_data.get('user_id')
    print('author data', author_data)
    defaults = {
        'email': author_data.get('email'),
        'username': author_data.get('username'),
        'url': author_data.get('url'),
        'github': author_data.get('github'),
        'profileImage': author_data.get('profileImage'),
        'host': author_data.get('host'),
        'displayName': author_data.get('displayName'),
    }
    AppUser.objects.update_or_create(user_id=user_id, defaults=defaults)


#get to get their authors stuff using their url 
#must have a 
def transform_author_data(raw_author, team_id):
    """
    Transforms raw author data to fit the AppUser model.
    Applies transformation based on the team_id.

    :param raw_author: The raw author data from the remote server.
    :param team_id: The team ID to determine specific transformation logic.
    :return: Transformed author data.
    """
    essential_fields = ['id', 'displayName', 'url', 'host']
    if not all(field in raw_author for field in essential_fields):
        return None 
    
    
    if team_id == 1:  # Assuming team 1 requires specific transformation
        username = raw_author.get('displayName', 'unknown')
        
        # print('all username,', username)
        email = f"{username}@email.com"

        data = {
            'user_id': raw_author.get('key'),
            'id': raw_author.get('id'),
            'username': raw_author.get('displayName'),
            'url': raw_author.get('url'),
            'github': raw_author.get('github'),
            'profileImage': raw_author.get('profileImage'),
            'host': raw_author.get('host'),
            'displayName': raw_author.get('displayName'),
            'email': email
        }
        # print('data transformed', data)
        return data 
    elif team_id == 2:
        # Handle other teams or default transformation
        pass

    return raw_author  


def identify_localauthor(author: AppUser):
    """
    will tell u if user is a local author
    """
    return author.host in LOCALHOSTS


def send_request_to_remoteInbox(follow_request:FriendRequest, object: AppUser):
    print('am here for requests')
    try:
        node = Node.objects.get(host=object.host)
    except:
        print(f"[ERROR]: no node for user {object.displayName, object.url }")
        return
    request_url = f'{object.url}inbox/'
    friendReq = FriendRequestSerializer(follow_request)
    friendReqData_toSend = friendReq.data
    print('friend remote request data', friendReqData_toSend)
    try:
        response = requests.post(request_url, json = friendReqData_toSend, auth=(node.username, node.password))
        if response.status_code == 200:
           print('succeeded sent friend requests')
    except requests.exceptions.RequestException as e:
        print(f"couldnt sent friend request to remote inbox{node.host}: {e}")
        

def send_post_toInbox(post: Post, user: AppUser, send_to_follower):
    """
    Send a post to the inbox of followers or all users.
    """
    recipients = user.followers.all() if send_to_follower else AppUser.objects.all()

    for recipient in recipients:
        try:
            if identify_localauthor(recipient):
                inbox, _ = Inbox.objects.get_or_create(authorId=recipient)
                inbox.posts.add(post)
            else:
                send_post_to_remoteInbox(post, recipient)
        except Exception as e:
            print(f'Error sending post to {recipient.url, recipient.displayName}: {e}')

def send_post_to_remoteInbox(post: Post, user: AppUser):
    try:
        node = Node.objects.get(host=user.host)
    except Exception as e:
        print(f"[ERROR]: No node for user {user.displayName, user.url}: {e}")
        return

    request_url = f'{user.url}inbox/'
    postReq = PostSerializer(post)
    postReqData_toSend = postReq.data
    try:
        response = requests.post(request_url, json=postReqData_toSend, auth=(node.username, node.password))
        if response.ok:
            print(f'Successfully sent post to global inbox {user.url}, {node.host}')
        else:
            print(f'Failed to send post: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f"Error sending post to remote inbox {node.host}: {e}")
