from django.shortcuts import render
from rest_framework import viewsets

from network.models import User, Tweet
from .serializers import CatSerializer
# Create your views here.
