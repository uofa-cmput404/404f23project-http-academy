import requests

csrf_token_url = "https://cmput404-http-academy-9e1478e268a7.herokuapp.com/get-csrf-token/"
login_url = "https://cmput404-http-academy-9e1478e268a7.herokuapp.com/authors/login"

session = requests.Session()
csrf_response = session.get(csrf_token_url)
csrf_token = csrf_response.json()['csrfToken']

email = "test"
password = "test"

auth_credentials = {"email": email, "password": password}
headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrf_token
}

login_response = session.post(
    login_url, json=auth_credentials, headers=headers)

if login_response.status_code == 200:
    print("API call successful!")
    print(login_response.json())
else:
    print(f"API call failed with status code: {login_response.status_code}")
    print(login_response.text)
