import os
from django.core.asgi import get_asgi_application
from django.conf import settings

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

import users.routing

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "advocate_management.settings"
)

django_asgi_app = get_asgi_application()

# ✅ CORRECT WAY TO SERVE STATIC FILES IN ASGI
django_asgi_app = ASGIStaticFilesHandler(django_asgi_app)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(users.routing.websocket_urlpatterns)
    ),
})
