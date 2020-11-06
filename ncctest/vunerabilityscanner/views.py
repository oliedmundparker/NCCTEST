from django.shortcuts import render
from rest_framework import viewsets

from .seralizers import ScanSerializer, VulnerabilitySerializer, UserSerializer, AssetsSerializer
from .models import Scan, Vulnerability, User, Assets

# Create your views here.


class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.all().order_by('id')
    serializer_class = ScanSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class AssetsViewSet(viewsets.ModelViewSet):
    queryset = Assets.objects.all().order_by('id')
    serializer_class = AssetsSerializer


class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all().order_by('id')
    serializer_class = VulnerabilitySerializer
