from centurion_crowdsale.payments.models import Payment
from centurion_crowdsale.invest_requests.models import InvestRequest
from centurion_crowdsale.vouchers.models import Voucher
from centurion_crowdsale.rates.models import UsdRate
from centurion_crowdsale.consts import DECIMALS
from centurion_crowdsale.settings import USD_MINIMAL_PURCHASE_BIAS


def parse_payment_message(message):
    tx_hash = message['transactionHash']
    if not Payment.objects.filter(tx_hash=tx_hash).count() > 0:
        rate_obj = UsdRate.objects.first()
        if not rate_obj:
            raise Exception('You should run rates_checker.py at least once')

        invest_request = InvestRequest.objects.get(id=message['exchangeId'])
        project = invest_request.project

        payment = Payment(
            invest_request=invest_request,
            currency=message['currency'],
            amount=message['amount'],
            tx_hash=tx_hash,
        )
        payment.save()

        usd_rate = getattr(rate_obj, payment.currency)
        usd_amount = payment.amount / DECIMALS[payment.currency] / usd_rate
        if usd_amount < invest_request.project.usd_minimal_purchase - USD_MINIMAL_PURCHASE_BIAS:
            print("NOT ENOUGH MONEY")
            return

        voucher = Voucher(
            project=project,
            payment=payment,
            usd_amount=f'{usd_amount:.{2}f}',
        )
        voucher.save()

        if payment.currency == 'DUC':
            project.duc_collected += payment.amount
            project.usd_collected_from_duc += voucher.usd_amount
        else:
            project.usd_collected_from_fiat += voucher.usd_amount

        try:
            voucher.send_mail()
            voucher.save()
        except Exception as e:
            print(repr(e))
    else:
        print(f'PARSING PAYMENT: tx {tx_hash} already registered', flush=True)
