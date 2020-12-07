from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from centurion_crowdsale.projects.serializers import CenturionProjectSerializer, CenturionProjectListSerializer
from centurion_crowdsale.projects.models import CenturionProject


class CenturionProjectView(APIView):
    @swagger_auto_schema(
        operation_description="Get project info",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_PATH, type=openapi.TYPE_STRING),
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER),
        ],
        responses={200: CenturionProjectSerializer()},
    )
    def get(self, request, category, id):
        project = CenturionProject.objects.get(category=category, project_id=id)
        serializer = CenturionProjectSerializer(project)
        return Response(serializer.data, status=200)


class CenturionProjectListView(APIView):
    @swagger_auto_schema(
        operation_description="Get project list from category",
        manual_parameters=[openapi.Parameter('category', openapi.IN_PATH, type=openapi.TYPE_STRING)],
        responses={200: CenturionProjectListSerializer()},
    )
    def get(self, request, category):
        # category = request.query_params['category']
        projects = CenturionProject.objects.filter(category=category)
        serializer = CenturionProjectListSerializer(projects, many=True)
        return Response(serializer.data, status=200)
