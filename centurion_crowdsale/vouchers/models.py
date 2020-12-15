from django.db import models
import secrets
from centurion_crowdsale.payments.models import Payment
from centurion_crowdsale.projects.models import CenturionProject
from centurion_crowdsale.transfers.models import Transfer
from centurion_crowdsale.quantum.models import QuantumCharge
from centurion_crowdsale.vouchers.voucher_email import html_style, voucher_html_body
from django.core.mail import send_mail
from django.core.mail import get_connection
from centurion_crowdsale.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_PASSWORD


class Voucher(models.Model):
    project = models.ForeignKey(CenturionProject, on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, null=True)
    quantum_charge = models.OneToOneField(QuantumCharge, on_delete=models.CASCADE, null=True)
    activation_code = models.CharField(max_length=50, unique=True, default=secrets.token_urlsafe)
    usd_amount = models.FloatField()
    is_used = models.BooleanField(default=False)
    is_email_sended = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    activation_date = models.DateTimeField(null=True, default=None)

    def send_mail(self):
        connection = get_mail_connection()
        html_body = voucher_html_body.format(
            tokens_purchased=self.usd_amount,
            project_leased=self.project.project_name,
            period_of_lease=self.project.staking_months,
            activate_code=self.activation_code
        )
        send_mail(
            'Centurion Lease Confirmation for ${}'.format(round(self.usd_amount, 2)),
            '',
            EMAIL_HOST_USER,
            [self.payment.invest_request.email if self.payment else self.quantum_charge.email],
            connection=connection,
            html_message=html_style + html_body,
        )
        self.is_email_sended = True
        self.save()

    def activate(self, address):
        try:
            token = self.project.token
        except Exception as e:
            return None

        token_amount = int(self.usd_amount * token.decimals)
        transfer = Transfer(
            voucher=self,
            amount=token_amount,
            currency=token.symbol,
            ducx_address=address,
        )
        try:
            transfer.tx_hash = token.mint(address, token_amount)
            transfer.status = 'WAITING FOR CONFIRM'
            self.is_used = True
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
