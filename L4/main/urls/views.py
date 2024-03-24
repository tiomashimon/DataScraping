from django.shortcuts import render
from .serializers import UrlSerializer
from .models import Url
from rest_framework.viewsets import ModelViewSet


class UrlViewSet(ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
