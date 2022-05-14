from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chatApp.routing

application = ProtocolTypeRouter(
    {'websocket': AuthMiddlewareStack(URLRouter(chatApp.routing.websocket_urlpatterns))}
)
