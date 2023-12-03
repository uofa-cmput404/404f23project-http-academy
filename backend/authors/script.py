
import requests
import json

csrf_token_url = "https://cmput404-httpacademy2-1c641b528836.herokuapp.com/authors/login"
login_url = "https://cmput404-httpacademy2-1c641b528836.herokuapp.com/authors/user"
post_url = "https://cmput404-httpacademy2-1c641b528836.herokuapp.com/posts/"
session = requests.Session()
print("Session:", session)

# credentials
email = "admin"
password = "admins"


data = {

    "post_id": "918f22b0-b849-415a-b57f-476add624a98",
    "id": None,
    "published": "2023-11-30T03:22:49.419571Z",
    "type": "post",
    "title": "http post",
    "content": "http poststs",
    "image": None,
    "count": 0,
    "source": "http://127.0.0.1:8000/",
    "origin": "http://127.0.0.1:8000/",
    "contentType": "text/plain",
    "visibility": "PUBLIC",
    "unlisted": False,
    "url": "http://127.0.0.1:8000/authors/49032c4c-c8e8-4f22-b6d6-1580f72c24d2/posts/918f22b0-b849-415a-b57f-476add624a98",
    "author": "49032c4c-c8e8-4f22-b6d6-1580f72c24d2",
    "categories": None,
    "comments": None,
    "likes": None

}

# Get CSRF token
csrf_response = session.post(
    csrf_token_url, json={'email': email, "password": password})
print("CSRF Response Status Code:", csrf_response.status_code)
print("CSRF Response JSON:", csrf_response.json())

csrf_token = csrf_response.json().get('csrf_token')
print("CSRF Token:", csrf_token)


header = {
    'X-CSRFToken': csrf_token
}

# Login request
login_response = session.get(login_url, headers=header)
print("Login Response Status Code:", login_response.status_code)

post_response = session.post(post_url, json=data, headers={
    'X-CSRFToken': csrf_token,
    'Referer': csrf_token_url
})

if post_response.status_code == 200:
    print("post call successful!")
    # THIS IS THE DATA TO RETRIEVE
    print("post Response JSON:", json.dumps(post_response.json(), indent=4))
    # Check if the user exists and has a valid password

else:
    # debugging stuff
    print(f"API call failed with status code: {post_response.status_code}")
    print("Login Response Text:", post_response.text)
    # Print out the response headers and cookies for debugging
    print("Response Headers:", post_response.headers)
    print("Response Cookies:", len(post_response.cookies))
