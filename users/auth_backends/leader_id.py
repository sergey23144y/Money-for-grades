from django.utils.http import urlencode
from social_core.backends.oauth import BaseOAuth2


class LeaderOAuth2(BaseOAuth2):
    """LeaderVKOAuth2 authentication backend"""
    name = 'leader-id-oauth2'
    ID_KEY = 'id'
    AUTHORIZATION_URL = 'https://leader-id.ru/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://leader-id.ru/oauth/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('id', 'user_id'),
        ('expires_in', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from VK.com account"""
        fullname, first_name, last_name = self.get_user_names(
            first_name=response['Data'].get('FirstName'),
            last_name=response['Data'].get('LastName')
        )
        return {'email': response['Data'].get('Email', ''),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = f'https://leader-id.ru/api/v4/api/v3/users/{kwargs["response"]["user_id"]}?' + urlencode({
            'access_token': access_token
        })
        return self.get_json(url)
