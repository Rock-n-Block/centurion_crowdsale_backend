from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.decorators import api_view
from centurion_crowdsale.quantum.models import QuantumCharge
from centurion_crowdsale.vouchers.models import Voucher
from centurion_crowdsale.projects.models import CenturionProject
from centurion_crowdsale.quantum.api import initiate_charge
from django.core.exceptions import ObjectDoesNotExist


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_STRING),
        ],
        properties={
            'usd_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['usd_amount', 'email']
    ),
    responses={"201": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "redirect_url": openapi.Schema(type=openapi.TYPE_STRING),
        }
    )},
)
@api_view(http_method_names=['POST'])
def create_charge(request, id):
    request_data = request.data
    usd_amount = request_data['usd_amount']
    email = request_data['email']

    charge_info = initiate_charge(usd_amount, email)
    project = CenturionProject.objects.get(string_id=id)

    charge = QuantumCharge(
        project=project,
        charge_id=charge_info['id'],
        status=charge_info['status'],
        usd_amount=usd_amount,
        hash=charge_info['hash'],
        redirect_url=charge_info['url'],
        email=email,
    )
    charge.save()

    return Response({"redirect_url": charge.redirect_url})


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'type': openapi.Schema(type=openapi.TYPE_STRING),
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                }),
        },
    ),
)
@api_view(http_method_names=['POST'])
def change_charge_status(request):
    request_data = request.data
    if request_data['type'] == 'Charge':
        status = request_data['data']['status']
        charge_id = request_data['data']['id']

        try:
            charge = QuantumCharge.objects.get(charge_id=charge_id)
        except ObjectDoesNotExist:
            print(f'Cannot find charge with id {charge_id} in database!', flush=True)
            return Response(200)

        if charge.status == 'Withdrawn':
            print(f'Voucher for charge with id {charge_id} was already created!', flush=True)
            return Response(200)

        charge.status = status
        charge.save()

        if status == 'Withdrawn':
            project = charge.project
            voucher = Voucher(
                project=project,
                quantum_charge=charge,
                usd_amount=charge.usd_amount,
                email=charge.email,
            )
            voucher.save()

            project.usd_collected_from_fiat += voucher.usd_amount
            project.save()

            try:
                voucher.send_mail()
                voucher.save()
            except Exception as e:
                print('Voucher email sending exception:', repr(e), flush=True)
    return Response(200)
