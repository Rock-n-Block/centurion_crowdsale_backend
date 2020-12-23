from rest_framework import serializers
from centurion_crowdsale.ducx_tokens.models import DucxToken


class DucxTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DucxToken
        fields = (
            'contract_address',
            'decimals',
            'symbol',
            'deploy_block'
        )
