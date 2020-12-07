from django.db import models
import secrets
from centurion_crowdsale.payments.models import Payment
from centurion_crowdsale.projects.models import CenturionProject
from centurion_crowdsale.settings import DUCX_NETWORK, IS_TESTNET, DRC20_TOKEN_ABI, GAS_LIMIT
from web3 import Web3, HTTPProvider
from centurion_crowdsale.settings_email import *
from django.core.mail import send_mail
from centurion_crowdsale.consts import MAX_AMOUNT_LEN
from django.core.mail import get_connection


w3 = Web3(HTTPProvider(DUCX_NETWORK['endpoint']))


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

    def transfer(self, address):
        token_amount = int(self.usd_amount * self.project.token_decimals)
        transfer = DucatusXNetworkTransfer(
            voucher=self,
            amount=token_amount,
            currency=self.project.token_symbol,
            ducx_address=address,
        )
        try:
            transfer.tx_hash = mint_tokens(self.project.token_contract_address, address, token_amount)
            transfer.status = 'WAITING FOR CONFIRM'
            self.is_used = True
            self.save()
        except Exception as e:
            transfer.tx_error = repr(e)
            transfer.status = 'FAIL'
        transfer.save()
        return transfer


class DucatusXNetworkTransfer(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=0)
    currency = models.CharField(max_length=10)
    ducx_address = models.CharField(max_length=50)
    tx_hash = models.CharField(max_length=100)
    tx_error = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='WAITING FOR TRANSFER')


def get_mail_connection():
    return get_connection(
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        use_tls=EMAIL_USE_TLS,
    )


def mint_tokens(contract_address, address, amount):
    contract = w3.eth.contract(address=contract_address, abi=DRC20_TOKEN_ABI)
    tx_params = {
        'nonce': w3.eth.getTransactionCount(DUCX_NETWORK['address'], 'pending'),
        'gasPrice': w3.eth.gasPrice,
        'gas': GAS_LIMIT,
    }
    initial_tx = contract.functions.mint(Web3.toChecksumAddress(address), amount).buildTransaction(tx_params)
    signed = w3.eth.account.signTransaction(initial_tx, DUCX_NETWORK['private'])
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    tx_hex = tx_hash.hex()
    return tx_hex






