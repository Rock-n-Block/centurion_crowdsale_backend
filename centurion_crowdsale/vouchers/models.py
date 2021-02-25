from django.db import models
import secrets
from centurion_crowdsale.transfers.models import Transfer
from centurion_crowdsale.vouchers.voucher_email import html_style, voucher_html_body
from django.core.mail import send_mail
from django.core.mail import get_connection
from django.utils import timezone
from centurion_crowdsale.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_PASSWORD


def voucher_code():
    return f'CF-{secrets.token_urlsafe()}'


class Voucher(models.Model):
    project = models.ForeignKey('projects.CenturionProject', on_delete=models.CASCADE)
    payment = models.OneToOneField('payments.Payment', on_delete=models.CASCADE, null=True, blank=True)
    quantum_charge = models.OneToOneField('quantum.QuantumCharge', on_delete=models.CASCADE, null=True, blank=True)
    activation_code = models.CharField(max_length=50, unique=True, default=voucher_code)
    usd_amount = models.DecimalField(max_digits=100, decimal_places=2)
    is_used = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    activation_datetime = models.DateTimeField(null=True, default=None, blank=True)
    email = models.CharField(max_length=50, default='', blank=True)

    def send_mail(self):
        connection = get_mail_connection()
        html_body = voucher_html_body.format(
            tokens_purchased=self.usd_amount,
            project_leased=self.project.project_name,
            period_of_lease=self.project.staking_months,
            activate_code=self.activation_code
        )
        send_mail(
            f'Your Lease Confirmation for ${self.usd_amount}',
            '',
            EMAIL_HOST_USER,
            [self.email],
            connection=connection,
            html_message=html_style + html_body,
        )
        self.is_email_sent = True
        self.save()

    def activate(self, address):
        token = self.project.token
        token_amount = int(self.usd_amount * (10 ** token.decimals))
        transfer = Transfer(
            voucher=self,
            amount=token_amount,
            currency=token.symbol,
            ducx_address=address,
        )
        try:
            transfer.tx_hash = token.transfer(address, token_amount)
            transfer.status = 'WAITING FOR CONFIRM'
            self.is_used = True
            self.activation_datetime = timezone.now()
            self.save()
        except Exception as e:
            transfer.tx_error = repr(e)
            transfer.status = 'FAIL'
        transfer.save()
        return transfer


def get_mail_connection():
    return get_connection(
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        use_tls=EMAIL_USE_TLS,
    )
