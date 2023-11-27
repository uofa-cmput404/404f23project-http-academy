import requests
import json

# csrf_token_url = "https://cmput404-httpacademy2-1c641b528836.herokuapp.com/authors/login"
# login_url = "https://cmput404-httpacademy2-1c641b528836.herokuapp.com/authors/user"
# access_url = "https://cmput404-httpacademy-local-cb3d56814192.herokuapp.com/authors/logout"

csrf_token_url = 'https://cmput404-social-network-401e4cab2cc0.herokuapp.com/auth/login/'
login_url = 'https://cmput404-social-network-401e4cab2cc0.herokuapp.com/authors/'
# access_url = "https://cmput404-httpacademy-local-cb3d56814192.herokuapp.com/authors/logout"
session = requests.Session()
print("Session:", session)

# credentials
email = "http-academy"
password = "cmput404"

# Get CSRF token
csrf_response = session.post(csrf_token_url, json={'username':email, "password":password})
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


# import requests
# import json

# # URLs
# login_url =  "https://cmput404-httpacademy-local-cb3d56814192.herokuapp.com/authors/login"
# logout_url = "https://cmput404-httpacademy-local-cb3d56814192.herokuapp.com/authors/logout"

# # Start a session
# session = requests.Session()

# # Credentials
# email = "admin@gmail.com"
# password = "admin"

# # Login request
# login_data = {'email': email, "password": password}
# login_response = session.post(login_url, data=login_data)

# if login_response.status_code == 200:
#     print("Login successful!")

#     # Access the logout page to retrieve CSRF token
#     logout_response = session.get(logout_url)
#     if logout_response.status_code == 200:
#         # Retrieve CSRF token from logout_response
#         # This part depends on how the CSRF token is provided in the logout page
#         # For example, it might be in a cookie or in the HTML
#         # csrf_token = csrf_response.json().get('csrf_token')
#         print("CSRF Token:", logout_response.headers)
#     else:
#         print("Failed to access logout page, status code:", logout_response.status_code)
# else:
#     # print("Login failed, status code:", login_response.headers)
#     logout_response = session.get(logout_url)
#     print('logout response', logout_response)
#     if logout_response.status_code == 200:
#         # Retrieve CSRF token from logout_response
#         # This part depends on how the CSRF token is provided in the logout page
#         # For example, it might be in a cookie or in the HTML
#         # csrf_token = csrf_response.json().get('csrf_token')
#         print("CSRF Token:", logout_response.headers)
