from rest_framework import serializers
from centurion_crowdsale.rates.models import UsdRate


class UsdRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsdRate
        fields = ('BTC', 'ETH', 'USDT', 'USDC')
