from django.db import models
import json
import requests
from centurion_crowdsale.settings import CRYPTOCOMPARE_API_KEY, CRYPTOCOMPARE_API_URL, DUCATUS_RATES_API_URL


class UsdRate(models.Model):
    BTC = models.FloatField()
    ETH = models.FloatField()
    USDC = models.FloatField()
    USDT = models.FloatField()
    DUC = models.FloatField()
    last_update_datetime = models.DateTimeField(auto_now=True)

    def update_rates(self):
        payload = {
            'fsym': 'USD',
            'tsyms': ['BTC', 'ETH', 'USDC', 'USDT'],
            'api_key': CRYPTOCOMPARE_API_KEY,
        }
        response = requests.get(CRYPTOCOMPARE_API_URL, params=payload)
        if response.status_code != 200:
            raise Exception(f'Cannot get exchange rates')
        response_data = json.loads(response.text)

        self.BTC = response_data['BTC']
        self.ETH = response_data['ETH']
        self.USDC = response_data['USDC']
        self.USDT = response_data['USDT']

        response = requests.get(DUCATUS_RATES_API_URL.format(fsym='USD', tsyms='DUC'))
        if response.status_code != 200:
            raise Exception(f'Cannot get DUC exchange rate')

        self.DUC = json.loads(response.content)['DUC']
