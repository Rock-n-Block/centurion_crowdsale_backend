from django.db import models
import requests
import json
from django.utils import timezone
from centurion_crowdsale.settings import QUANTUM_CLIENT_SECRET, QUANTUM_CLIENT_ID, QUANTUM_API_URL, \
    QUANTUM_SESSION_TIMEOUT_IN_SECS


class QuantumAccess(models.Model):
    access_token = models.TextField(null=True)
    token_type = models.CharField(max_length=20, null=True)
    token_expires_at = models.BigIntegerField(null=True)

    def update(self):
        token_expiration_delta = (self.token_expires_at or 0) + QUANTUM_SESSION_TIMEOUT_IN_SECS
        if token_expiration_delta < timezone.now().timestamp():
            request_data = {
                'client_id': QUANTUM_CLIENT_ID,
                'client_secret': QUANTUM_CLIENT_SECRET,
                'grant_type': 'client_credentials',
            }
            new_token_request = requests.post(QUANTUM_API_URL.format('connect/token'), data=request_data)
            token_info = json.loads(new_token_request.content)

            self.token_type = token_info['token_type']
            self.access_token = token_info['access_token']
            self.token_expires_at = timezone.now().timestamp() + token_info['expires_in']
            self.save()


class QuantumCharge(models.Model):
    project = models.ForeignKey('projects.CenturionProject', on_delete=models.CASCADE, null=True, blank=True)
    charge_id = models.IntegerField(unique=True)
    status = models.CharField(max_length=50)
    usd_amount = models.DecimalField(max_digits=100, decimal_places=2)
    hash = models.CharField(max_length=100)
    redirect_url = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    last_update_datetime = models.DateTimeField(auto_now=True)
