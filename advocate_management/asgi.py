from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from users.middleware import JWTAuthMiddleware
import users.routing
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "advocate_management.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(users.routing.websocket_urlpatterns)
    ),
})
