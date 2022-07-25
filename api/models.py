from django.db import models


class Urls(models.Model):
    short_url = models.CharField(max_length=16)
    long_url = models.CharField(max_length=256)
