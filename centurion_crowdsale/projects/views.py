from centurion_crowdsale.projects.serializers import CenturionProjectSerializer
from centurion_crowdsale.projects.models import CenturionProject
from rest_framework import viewsets, mixins


class CenturionProjectViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CenturionProject.objects.all()
    serializer_class = CenturionProjectSerializer





