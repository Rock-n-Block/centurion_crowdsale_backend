from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from centurion_crowdsale.invest_requests.models import InvestRequest
from centurion_crowdsale.projects.models import CenturionProject
from centurion_crowdsale.invest_requests.serializers import InvestRequestSerializer
from centurion_crowdsale.settings import DUC_RATE
import decimal


validate_usd_amount_result = openapi.Response(
    description='status of validated USD amount: `FEW`, `OK` or `MUCH`',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)


class InvestRequestView(APIView):
    @swagger_auto_schema(
        operation_description="post email address and get addresses for payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            manual_parameters=[
                openapi.Parameter('string_id', openapi.IN_PATH, type=openapi.TYPE_STRING),
            ],
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={201: InvestRequestSerializer()},
    )
    def post(self, request, string_id):
        request_data = request.data
        print(f'INVEST REQUEST data: {request_data}', flush=True)
        email = request_data['email']
        project = CenturionProject.objects.get(string_id=string_id)

        invest_request = InvestRequest(email=email, project=project)
        invest_request.save()
        invest_request.generate_keys()
        invest_request.save()

        serializer = InvestRequestSerializer(invest_request)
        return Response(serializer.data, status=201)


class ValidateUsdAmountView(APIView):
    @swagger_auto_schema(
        operation_description="post USD amount to check if DUC limit is exceeded",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            manual_parameters=[
                openapi.Parameter('string_id', openapi.IN_PATH, type=openapi.TYPE_STRING),
            ],
            required=['usd_amount', 'currency'],
            properties={
                'usd_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                'currency': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: validate_usd_amount_result},
    )
    def post(self, request, string_id):
        data = request.data
        usd_amount = decimal.Decimal(data['usd_amount'])
        currency = data['currency']
        project = CenturionProject.objects.get(string_id=string_id)

        if currency == 'DUC':
            if usd_amount < project.usd_minimal_purchase:
                status = 'FEW'
            elif usd_amount + project.usd_collected_from_duc > project.usd_from_duc_target_raise:
                status = 'MUCH'
            else:
                status = 'OK'
        else:
            if usd_amount < project.usd_minimal_purchase:
                status = 'FEW'
            elif usd_amount + project.usd_collected_from_duc > project.usd_from_fiat_target_raise:
                status = 'MUCH'
            else:
                status = 'OK'

        return Response({'status': status}, status=200)
