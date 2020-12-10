from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from centurion_crowdsale.projects.serializers import CenturionProjectSerializer, CenturionProjectListSerializer
from centurion_crowdsale.projects.models import CenturionProject
from rest_framework.exceptions import ValidationError


class CenturionProjectView(APIView):
    @swagger_auto_schema(
        operation_description="Get project info",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_STRING),
        ],
        responses={200: CenturionProjectSerializer()},
    )
    def get(self, request, id):
        project = CenturionProject.objects.get(string_id=id)
        serializer = CenturionProjectSerializer(project)
        return Response(serializer.data, status=200)

    def delete(self, request, id):
        project = CenturionProject.objects.get(string_id=id)
        project.delete()
        return Response(status=204)


class CenturionProjectsView(APIView):
    @swagger_auto_schema(
        operation_description="Get project list",
        responses={200: CenturionProjectListSerializer()},
    )
    def get(self, request):
        categories = [person.category for person in CenturionProject.objects.all()]
        response = {}
        for category in categories:
            projects = CenturionProject.objects.filter(category=category)
            response[category] = CenturionProjectListSerializer(projects, many=True).data
        return Response(response, status=200)

    @swagger_auto_schema(
        operation_description="Add project to database",
        request_body=CenturionProjectSerializer,
        responses={201: CenturionProjectSerializer()},

    )
    def post(self, request):
        serializer = CenturionProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError(detail={'description': serializer.errors, 'project': request.data})

        return Response(serializer.data, status=201)



