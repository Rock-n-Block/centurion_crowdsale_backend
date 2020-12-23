from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from centurion_crowdsale.projects.serializers import CenturionProjectSerializer
from centurion_crowdsale.projects.models import CenturionProject
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CenturionProjectViewSet(viewsets.ModelViewSet):
    queryset = CenturionProject.objects.all()
    serializer_class = CenturionProjectSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]





