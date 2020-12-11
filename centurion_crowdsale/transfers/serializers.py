from rest_framework import serializers
from centurion_crowdsale.transfers.models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'