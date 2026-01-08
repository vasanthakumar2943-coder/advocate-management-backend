from django.urls import path
from .views import signup, login_view, me

urlpatterns = [
    path("signup/", signup),
    path("login/", login_view),
    path("me/", me),
]
