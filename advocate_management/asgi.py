import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from whitenoise import WhiteNoise
from django.conf import settings

import users.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "advocate_management.settings")

django_asgi_app = get_asgi_application()

# ✅ CORRECT STATIC ROOT (NO HARD-CODE)
django_asgi_app = WhiteNoise(
    django_asgi_app,
    root=str(settings.STATIC_ROOT),
    prefix=settings.STATIC_URL,
)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(users.routing.websocket_urlpatterns)
    ),
})
