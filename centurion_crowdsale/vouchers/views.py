from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from centurion_crowdsale.vouchers.models import Voucher
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response


activation_success_response = openapi.Response(
    description='response with transaction hash if token transfer was successful',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'tx_hash': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)

activation_fail_response = openapi.Response(
    description='voucher activation fail cause: `USED`, `EXPIRED` or `TRANSFER FAIL`',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)

not_found_response = openapi.Response(
    description='response if no such voucher exists',
)


class VoucherActivationView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'activation_code': openapi.Schema(type=openapi.TYPE_STRING),
                'ducx_address': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['activation_code', 'ducx_address']
        ),
        responses={200: activation_success_response, 403: activation_fail_response, 404: not_found_response},
    )
    def post(self, request):
        request_data = request.data
        activation_code = request_data['activation_code']
        ducx_address = request_data['ducx_address']

        try:
            voucher = Voucher.objects.get(activation_code=activation_code)
        except ObjectDoesNotExist:
            return Response(status=404)

        if voucher.is_used:
            return Response({'detail': 'USED'}, status=403)

        if voucher.project.is_staking_finished:
            return Response({'detail': 'EXPIRED'}, status=403)

        tx_hash = voucher.activate(ducx_address)
        voucher.save()
        if tx_hash:
            return Response({'tx_hash': tx_hash}, status=200)
        else:
            return Response({'detail': 'TRANSFER FAIL'}, status=403)
