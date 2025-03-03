from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AnonymousUser


class TokenAuthenticationMiddleware(BaseMiddleware):
    def __init__(self, *args, **kwargs):
        self.token = None
        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send):
        # extract the token from the 'Authorization' header
        for header, value in scope.get("headers", []):
            if header == b"authorization":
                # extract token part
                self.token = value.decode("utf-8").split(" ")[1]
                break
        if self.token:
            scope["user"] = await self.get_user(token=self.token)
        else:
            scope["user"] = AnonymousUser()

        if isinstance(scope["user"], AnonymousUser):
            await send(
                {
                    "type": "websocket.close",
                    "code": 4000,
                }
            )
            return
        await super().__call__(scope, receive, send)

    async def get_user(self, token):
        try:
            token_obj = await Token.objects.select_related(
                "user",
            ).aget(key=token)
            return token_obj.user
        except Token.DoesNotExist:
            return AnonymousUser()
