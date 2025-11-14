import requests
from social_core.backends.oauth import BaseOAuth2 # type: ignore
from django.conf import settings

class Auth0(BaseOAuth2):
    name = 'auth0'
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False

    def authorization_url(self):
        return f"https://{self.setting('DOMAIN')}/authorize"

    def access_token_url(self):
        return f"https://{self.setting('DOMAIN')}/oauth/token"

    def get_user_id(self, details, response):
        return details['user_id']

    def get_user_details(self, response):
        url = f"https://{self.setting('DOMAIN')}/userinfo"
        headers = {'authorization': f"Bearer {response['access_token']}"}
        resp = requests.get(url, headers=headers)
        userinfo = resp.json()
        
        return {
            'username': userinfo['nickname'],
            'email': userinfo['email'],
            'first_name': userinfo['name'],
            'user_id': userinfo['sub'],
        }

def getRole(request):
    if not request.user.is_authenticated:
        return None
        
    try:
        auth0_user = request.user.social_auth.get(provider='auth0')
        accessToken = auth0_user.extra_data['access_token']
        url = f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/userinfo"
        headers = {'authorization': f"Bearer {accessToken}"}
        
        resp = requests.get(url, headers=headers)
        userinfo = resp.json()
        role = userinfo.get(f"{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/role", "Usuario")
        return role
    except:
        return "Usuario"