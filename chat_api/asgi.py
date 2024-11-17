from channels.routing import URLRouter,ProtocolTypeRouter
import os
from chat.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application

from .middleware import JWTAuthMiddleware
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_api.settings')

application = ProtocolTypeRouter({
"http":get_asgi_application(),
"websocket":
        JWTAuthMiddleware(URLRouter(websocket_urlpatterns))
    })