from django.db import models


class Url(models.Model):
    url = models.CharField(max_length=255)