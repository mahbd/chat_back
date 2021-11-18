from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': URLRouter(chat.routing.websocket_urlpatterns),
})