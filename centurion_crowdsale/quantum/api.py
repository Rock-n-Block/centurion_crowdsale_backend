from centurion_crowdsale.quantum.models import QuantumAccess
from centurion_crowdsale.settings import QUANTUM_RECEIVER_ADDRESS, QUANTUM_REDIRECT_URL, QUANTUM_API_URL
import requests
import json


def initiate_charge(amount, email):
    quantum_access = QuantumAccess.objects.first() or QuantumAccess()
    quantum_access.update()
    quantum_access.save()

    new_charge_data = {
        'amount': {
            'currencyCode': 'USD',
            'value': amount,
        },
        'email': email,
        'tokenCurrencyCode': 'QUSD',
        'receivingAccountAddress': QUANTUM_RECEIVER_ADDRESS,
        'returnUrl': QUANTUM_REDIRECT_URL,
    }

    headers = {
        'Authorization': '{token_type} {access_token}'.format(token_type=quantum_access.token_type,
                                                              access_token=quantum_access.access_token)
    }

    creation_request = requests.post(QUANTUM_API_URL.format('api/v1/merchant/charges'),
                                     json=new_charge_data,
                                     headers=headers)

    return json.loads(creation_request.content)


