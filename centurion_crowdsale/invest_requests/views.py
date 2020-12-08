from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from centurion_crowdsale.invest_requests.models import InvestRequest
from centurion_crowdsale.projects.models import CenturionProject
from centurion_crowdsale.invest_requests.serializers import InvestRequestSerializer
from centurion_crowdsale.settings import DUC_RATE


validate_usd_from_duc_amount_result = openapi.Response(
    description='status of validated USD amount',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'amount_valid': openapi.Schema(type=openapi.TYPE_BOOLEAN)
        },
    )
)


class InvestRequestView(APIView):
    @swagger_auto_schema(
        operation_description="post email address and get addresses for payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            manual_parameters=[
                openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER),
            ],
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={201: InvestRequestSerializer()},
    )
    def post(self, request, id):
        request_data = request.data
        print(f'INVEST REQUEST data: {request_data}', flush=True)
        email = request_data['email']
        project = CenturionProject.objects.get(id=id)
        invest_request = get_or_create_invest_request(email, project)

        serializer = InvestRequestSerializer(invest_request)
        return Response(serializer.data, status=201)


class ValidateUsdFromDucAmountView(APIView):
    @swagger_auto_schema(
        operation_description="post USD amount to check if DUC limit is exceeded",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            manual_parameters=[
                openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER),
            ],
            required=['usd_amount'],
            properties={
                'usd_amount': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={200: validate_usd_from_duc_amount_result},
    )
    def post(self, request, id):
        usd_amount = request.data['usd_amount']
        duc_amount = usd_amount / DUC_RATE
        project = CenturionProject.objects.get(id=id)

        return Response({'amount_valid': duc_amount + float(project.duc_collected) <= project.duc_target_raise}, status=201)


def get_or_create_invest_request(email, project):
    invest_request_filter = InvestRequest.objects.filter(email=email, project=project)
    if not invest_request_filter:
        invest_request = InvestRequest(email=email, project=project)
        invest_request.save()
        invest_request.generate_keys()
        invest_request.save()
    else:
        invest_request = invest_request_filter.first()
    return invest_request
