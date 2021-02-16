from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from centurion_crowdsale.vouchers.models import Voucher
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.utils import timezone
import requests
import json


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

        print(f'VOUCHER ACTIVATION: received activation code {activation_code} from {ducx_address}', flush=True)

        duc_back_response = requests.post('https://www.ducatuscoins.com/api/v3/transfer/', data=request_data)
        status = duc_back_response.status_code

        if status != 500:
            data = json.loads(duc_back_response.content)
            if status == 403 and data['detail'] == "Invalid activation code":
                pass
            else:
                return Response(data, status=status)

        try:
            voucher = Voucher.objects.get(activation_code=activation_code)
        except ObjectDoesNotExist:
            print(f'VOUCHER ACTIVATION: voucher {activation_code} doesn`t exist', flush=True)
            return Response(status=404)

        if voucher.is_used:
            print(f'VOUCHER ACTIVATION: voucher {activation_code} has already been used', flush=True)
            return Response({'detail': 'USED'}, status=403)

        if voucher.project.raise_start_datetime is not None and timezone.now() > voucher.project.staking_finish_datetime:
            print(f'VOUCHER ACTIVATION: voucher {activation_code} expired', flush=True)
            return Response({'detail': 'EXPIRED'}, status=403)

        transfer = voucher.activate(ducx_address)
        voucher.save()
        token_amount = transfer.amount / (10 ** voucher.project.token.decimals)
        if transfer.tx_hash:
            print(f'VOUCHER ACTIVATION: Successful transfer {transfer.tx_hash} to {transfer.ducx_address} '
                  f'for {token_amount} {transfer.currency}', flush=True)
            return Response({'tx_hash': transfer.tx_hash}, status=200)
        else:
            print(f'VOUCHER ACTIVATION: Failed transfer {token_amount} {transfer.currency} to {transfer.ducx_address} '
                  f'with exception {transfer.tx_error}', flush=True)
            return Response({'detail': 'TRANSFER FAIL'}, status=403)
