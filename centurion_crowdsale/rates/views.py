from rest_framework.views import APIView
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from centurion_crowdsale.rates.models import UsdRate
from centurion_crowdsale.rates.serializers import UsdRateSerializer


class UsdRateView(APIView):
    @swagger_auto_schema(
        operation_description="Get USD rates",
        responses={200: UsdRateSerializer()},
    )
    def get(self, request):
        rate = UsdRate.objects.first()
        serializer = UsdRateSerializer(rate)
        return Response(serializer.data, status=200)
