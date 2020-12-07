from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from centurion_crowdsale.vouchers.models import Voucher
from centurion_crowdsale.vouchers.serializers import DucatusXNetworkTransferSerializer
from rest_framework.exceptions import PermissionDenied, APIException
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response


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
        responses={200: DucatusXNetworkTransferSerializer()},
    )
    def post(self, request):
        activation_code = request.data['activation_code']
        ducx_address = request.data['ducx_address']
        try:
            voucher = Voucher.objects.get(activation_code=activation_code)
            # TODO: implement
            if voucher.is_used:
                pass
            '''
            if not voucher.is_active:
                raise PermissionDenied(detail='This voucher is not active')
            if voucher.is_used:
                raise PermissionDenied(detail='This voucher already used')
            '''
            transfer = voucher.transfer(ducx_address)
            serializer = DucatusXNetworkTransferSerializer(transfer)
            return Response(serializer.data, status=200)
        except ObjectDoesNotExist:
            raise PermissionDenied(detail='Invalid activation code')
