import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from whitenoise import WhiteNoise

import users.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "advocate_management.settings")

django_asgi_app = get_asgi_application()

# 🔥 WhiteNoise wraps ASGI app (THIS FIXES ADMIN CSS)
django_asgi_app = WhiteNoise(
    django_asgi_app,
    root="/app/staticfiles",
    prefix="static/",
)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(users.routing.websocket_urlpatterns)
    ),
})
