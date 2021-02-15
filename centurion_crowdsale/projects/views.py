from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from centurion_crowdsale.projects.serializers import CenturionProjectSerializer, CenturionProjectListSerializer
from centurion_crowdsale.projects.models import CenturionProject


class CenturionProjectView(APIView):
    @swagger_auto_schema(
        operation_description="Get project info",
        manual_parameters=[
            openapi.Parameter('string_id', openapi.IN_PATH, type=openapi.TYPE_STRING),
        ],
        responses={200: CenturionProjectSerializer()},
    )
    def get(self, request, string_id):
        try:
            project = CenturionProject.objects.get(string_id=string_id)
        except CenturionProject.DoesNotExist:
            return Response(status=404)

        serializer = CenturionProjectSerializer(project)
        return Response(serializer.data, status=200)


class CenturionProjectsView(APIView):
    @swagger_auto_schema(
        operation_description="Get list of projects by category",
        responses={200: CenturionProjectListSerializer()},
    )
    def get(self, request):
        categories = [project.category for project in CenturionProject.objects.all()]
        response = {}
        for category in categories:
            projects = CenturionProject.objects.filter(category=category)
            response[category] = CenturionProjectListSerializer(projects, many=True).data
        return Response(response, status=200)
