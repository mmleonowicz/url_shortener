from django.urls import path
from .views import shorten_url, redirect_to_url

urlpatterns = [
    path("", shorten_url, name="shorten"),
    path("<str:short_url>/", redirect_to_url, name="redirect_short"),
]
