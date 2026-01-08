import os
from django.core.asgi import get_asgi_application
from django.conf import settings

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from whitenoise import WhiteNoise

import users.routing

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "advocate_management.settings"
)

# Django ASGI application
django_asgi_app = get_asgi_application()

# ✅ WhiteNoise (STATIC FILES FIX)
django_asgi_app = WhiteNoise(
    django_asgi_app,
    root=str(settings.STATIC_ROOT),
    prefix=settings.STATIC_URL,
)

# ✅ FINAL ASGI APPLICATION
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(users.routing.websocket_urlpatterns)
    ),
})
