from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from src.apps.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs


@database_sync_to_async
def get_user(token):
    try:
        # Decode the token to get the payload
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        
        # Get the user based on the ID
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        print(user)
        return user
    except Exception as e:
        return None



class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:

            params = parse_qs(scope["query_string"].decode())

            token = params.get('authorization', [None])[0]
            if isinstance(token, str) and "Bearer" in token:
                token = token.split("Bearer")[1]
                if isinstance(token, str) and " " or "%20" in token:
                    token = token.replace(" ", "")
                    token = token.replace("%20", "")

        except Exception as e:

            token = None

        if token is not None:
            user = await get_user(token)
            if user is not None:
                scope["user"] = user
            else:
                scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
