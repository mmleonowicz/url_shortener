"""Handles all url shortener logic"""
import random
import string
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Urls


@api_view(["POST"])
def shorten_url(request):
    """Takes 'POST' method. Converts 'long_url' from request to
    'short_url' and returns both in the response.
    :return: A http response
    :rtype: Response(dict)
    """
    data = request.data
    short_url = "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase + string.digits, k=8
        )
    )
    long_url = data["long_url"]
    Urls.objects.create(long_url=long_url, short_url=short_url)
    short_url = f'{request.build_absolute_uri(reverse("shorten"))}{short_url}'
    return Response({"long_url": long_url, "short_url": short_url})


def redirect_to_url(request, short_url):
    """Queries for 'short_url' and redirects to 'long_url' if found in
    database.
    :param short_url: Shortened version of 'long_url'
    :type: str
    :return: Redirect to 'long_url'
    """
    try:
        url = Urls.objects.get(short_url=short_url)
    except Urls.DoesNotExist:
        return HttpResponse(status=404)

    return redirect(url.long_url)
