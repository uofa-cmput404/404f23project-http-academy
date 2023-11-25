import requests
import json

csrf_token_url = "http://127.0.0.1:8000/authors/login"
login_url = "http://127.0.0.1:8000/authors/user"

session = requests.Session()
print("Session:", session)

# credentials
email = "oliver@gmail.com"
password = "ogo12345"

# Get CSRF token
csrf_response = session.post(csrf_token_url, json={'email':email, "password":password})
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

if login_response.status_code == 200:
    print("API call successful!")
    print("Login Response JSON:", json.dumps(login_response.json(),indent=4)) # THIS IS THE DATA TO RETRIEVE
    # Check if the user exists and has a valid password
    
else:
    # debugging stuff
    print(f"API call failed with status code: {login_response.status_code}")
    print("Login Response Text:", login_response.text)
    # Print out the response headers and cookies for debugging
    print("Response Headers:", login_response.headers)
    print("Response Cookies:", len(login_response.cookies))
