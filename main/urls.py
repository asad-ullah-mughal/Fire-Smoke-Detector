from django.urls import path
from .views import *

urlpatterns = [
    path("", landing, name="landing"),
    path("index/", index, name="index"),
    path("upload/", upload, name="upload"),
    path("camera/", camera, name="camera"),
    path("live_feed/", live_feed, name="live_feed"),  # ✅ New live stream route
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
