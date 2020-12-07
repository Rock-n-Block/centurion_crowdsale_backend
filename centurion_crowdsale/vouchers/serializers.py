from rest_framework import serializers
from centurion_crowdsale.vouchers.models import DucatusXNetworkTransfer


class DucatusXNetworkTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = DucatusXNetworkTransfer
        fields = '__all__'