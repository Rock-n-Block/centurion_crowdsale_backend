from django.db import models
import secrets
from centurion_crowdsale.payments.models import Payment
from centurion_crowdsale.projects.models import CenturionProject
from centurion_crowdsale.transfers.models import Transfer
from centurion_crowdsale.settings_email import *
from django.core.mail import send_mail
from django.core.mail import get_connection


class Voucher(models.Model):
    project = models.ForeignKey(CenturionProject, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    activation_code = models.CharField(max_length=50, unique=True, default=secrets.token_urlsafe)
    usd_amount = models.FloatField()
    is_used = models.BooleanField(default=False)
    is_email_sended = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    activation_date = models.DateTimeField(null=True, default=None)

    def send_mail(self):
        connection = get_mail_connection()
        html_body = voucher_html_body.format(
            voucher_code=self.activation_code
        )
        send_mail(
            'Your DUC Purchase Confirmation for ${}'.format(round(self.usd_amount, 2)),
            '',
            EMAIL_HOST_USER,
            [self.payment.invest_request.email],
            connection=connection,
            html_message=warning_html_style + html_body,
        )
        self.is_email_sended = True

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







