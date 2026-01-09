from requests_oauthlib import OAuth2Session
import os


CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", " ")
CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", " ")
REDIRECT_URI = "http://localhost:8000/callback"
AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
SCOPE = ["read:user"]


oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
print("Перейдите по ссылке для авторизации:", authorization_url)


authorization_response = input("Введите полный URL редиректа: ")


token = oauth.fetch_token(
    TOKEN_URL,
    authorization_response=authorization_response,
    client_secret=CLIENT_SECRET 
)

print("Токен получен:", token)


user_info = oauth.get("https://api.github.com/user")
print("Информация о пользователе:", user_info.json())
