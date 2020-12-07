from rest_framework import serializers
from centurion_crowdsale.invest_requests.models import InvestRequest


class InvestRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestRequest
        fields = ('eth_address', 'btc_address', 'duc_address')
