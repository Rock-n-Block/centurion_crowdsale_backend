from django.db import models
from centurion_crowdsale.invest_requests.models import InvestRequest
from centurion_crowdsale.consts import MAX_AMOUNT_LEN


class Payment(models.Model):
    invest_request = models.ForeignKey(InvestRequest, on_delete=models.CASCADE, null=True)
    tx_hash = models.CharField(max_length=100)
    currency = models.CharField(max_length=50)
    amount = models.CharField(max_length=MAX_AMOUNT_LEN)
