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
from authors.serializers import UserSerializer
from followers.models import FriendRequest
from followers.serializers import FriendRequestSerializer
from posts.models import Post
from inbox.models import Inbox
from posts.serializers import PostSerializer
import json
from posts.models import Comment
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
            response = requests.get(
                request_url, auth=(node.username, node.password))
            if response.status_code == 200:
                remoteAuthors = response.json().get('items', [])
                print('remote authors', json.dumps(response.json(), indent=4))
                for raw_author in remoteAuthors:
                    transformed_author = transform_author_data(
                        raw_author, node.team)
                    # print('remote author', transformed_author)

                    # Update or create the author in the database
                    create_or_update_author(transformed_author)
                    allAuthors.append(transformed_author)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching authors from {remoteHost}: {e}")
            return allAuthors

    return allAuthors


def fetchRemotePosts():
    print('fetching remote posts')
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
        try:
            response = requests.get(
                request_url, auth=(node.username, node.password))
            print('response from other team 2', json.dumps(response.json()))
            if response.status_code == 200:
                remotePosts = response.json().get()
                # print('remote posts', json.dumps(response.json(), indent = 4))
                for raw_post in remotePosts:
                    transformed_post = transform_post_data(raw_post, node.team)
                #     # print('remote author', transformed_author)

                #     # Update or create the author in the database
                #     create_or_update_author(transformed_author)
                #     allAuthors.append(transformed_author)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching authors from {remoteHost}: {e}")
            return allPosts

    return allPosts


def transform_post_data(raw_post, team_id):

    if team_id == 1:  # Assuming team 1 requires specific transformation
        username = raw_post.get('displayName', 'unknown')

        # print('all username,', username)
        email = f"{username}@email.com"


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


# get to get their authors stuff using their url
# must have a
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
    return author.isForeign == False


def send_request_to_remoteInbox(follow_request: FriendRequest, object: AppUser):
    print('am here for rmeote requests', object.host)
    # try:
    #     node = Node.objects.get(host=object.host)
    # except:
    #     print(f"[ERROR]: no node for user {object.displayName, object.url }")
    #     return
    username = "admin"
    password = "admin"
    base, author_id = object.url.rsplit('authors', 1)
    request_url = f'{base}service/authors{author_id}/inbox/'

    print('request url', request_url)
    friendReq = FriendRequestSerializer(follow_request)
    friendReqData_toSend = friendReq.data
    print('friend remote request data', friendReqData_toSend)
    try:
        response = requests.post(
            request_url, json=friendReqData_toSend, auth=(username, password))
        print('status code response', response.status_code)
        if response.status_code == 200:
            print('succeeded sent friend requests')
    except requests.exceptions.RequestException as e:
        print(f"couldnt sent friend request to remote inbox: {e}")


def send_remoteUser(user: AppUser):
    """
    send all our users upon creation to remote team 
    """

    host_rm = "https://whowill-648a6cd76980.herokuapp.com/"
    # try:
    #     node = Node.objects.get(host=object.host)
    # except:
    #     print(f"[ERROR]: no node for user {object.displayName, object.url }")
    #     return
    base, author_id = user.url.rsplit('authors', 1)
    print('user ready to send to the remote')
    print(base, author_id)
    print('user to send to whoiswill', user)

    data = {
        "type": "author",
        "id": user.id,
        "host": user.host,
        "email": user.email,
        "displayName": user.username,
        "github": "http://github.com/laracroft",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    }

    request_url = f'{host_rm}service/authors{author_id}/'
    username = "admin"
    password = "admin"
    try:
        response = requests.post(
            request_url, json=data, auth=(username, password))
        print('status code response', response.status_code)
        if response.status_code == 200:
            print('succeeded sending users')
    except requests.exceptions.RequestException as e:
        print(f"couldnt sent friend request to remote database")


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
            print(
                f'Error sending post to {recipient.url, recipient.displayName}: {e}')


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
        response = requests.post(
            request_url, json=postReqData_toSend, auth=(node.username, node.password))
        if response.ok:
            print(
                f'Successfully sent post to global inbox {user.url}, {node.host}')
        else:
            print(f'Failed to send post: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f"Error sending post to remote inbox {node.host}: {e}")


def sendComment_toRemoteHost(comment: Comment, user: AppUser):
    host_account = "https://whowill-648a6cd76980.herokuapp.com/"
    username = "admin"
    password = "admin"

    # Convert UUID objects to strings
    comment_id_str = str(
        comment["postId"]) if 'postId' in comment and comment['postId'] is not None else None
    user_id_str = str(user.id)

    commentData = {
        "type": "comment",
        "author": {
            "id": user_id_str,
        },
        "comment": comment.get('comment', ''),
        "contentType": comment.get('contentType', ''),
        "published": comment.get('published', ''),
        "id": comment_id_str,
    }

    # Construct the request URL
    request_url = f"{host_account}service/authors/{user_id_str}/posts/{comment_id_str}/comments"
    print('comment data to send to whoiswill', commentData)

    # Send the POST request
    try:
        response = requests.post(
            request_url, json=commentData, auth=(username, password))
        if response.ok:
            print('Successfully sent comment to who is will')
        else:
            print(f'Failed to send post: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f"Error sending comment to who is will: {e}")


def testsend_post_to_remoteInbox(post: Post, user: AppUser):
    host_account = "https://whowill-648a6cd76980.herokuapp.com/"
    username = "admin"
    password = "admin"
    # try:
    #     node = Node.objects.get(host=host_account)
    # except Exception as e:
    #     print(f"[ERROR]: No node for user {user.displayName, user.url}: {e}")
    #     return
    # print('node gotten', node)
    base, author_id = user.url.rsplit('authors', 1)
    request_url = f"https://whowill-648a6cd76980.herokuapp.com/service/authors{author_id}/posts/"

    print('request url', request_url)
    source_rm = post.source
    origin_rm = post.origin
    title_rm = post.title
    contentType_rm = post.contentType
    visibility_rm = post.visibility
    content_rm = post.content
    id_rm = post.id
    published_rm = post.published.isoformat() if post.published else None
    unlisted_rm = post.unlisted
    image_rm = post.image
    data_2 = {
        "type": "post",
        "title": title_rm,
        "id": id_rm,
        "description": "",
        "contentType": contentType_rm,
        "content": "TEST Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
        "source": source_rm,
        "origin": origin_rm,
        "contentType": contentType_rm,
        "content": content_rm,
        "author": {
            "id": user.id,
        },
        "categories": [],
        "image": image_rm,

        "published": published_rm,
        "visibility": visibility_rm,
        "unlisted": unlisted_rm
    }

    print('data to send', data_2)
    print('data to send', type(data_2.get("title")))
    print('Source', type(data_2.get("source")))
    print('origin', type(data_2.get("origin")))
    # postID = post["id"].split("/").pop()

    # post["author"] = str(post['author'])

    try:
        response = requests.post(
            request_url, json=data_2, auth=(username, password))
        if response.ok:
            print('response ', response.json())
            print(
                f'Successfully sent post to who is will {response.status_code}')
        else:
            print(f'Failed to send post: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f"Error sending post to who is will")


# edge case - users old posts prior to following another user
# send all posts upon creation, can update other teams server once user gets to following them


""""
    server 1 

        
        (4:16) user 1  -> send friend req to user 2
        
    
    server 2    - > receives friend req in inbox 
                    -> can choose to accept/reject friend req
                        -> if accept (user 1 in following list of user 2 )
        4:13 posts before rrquest:
            [first post, second post]
        user 2  accepts friend requests
        posts after rrquest:
            [third post]
"""
