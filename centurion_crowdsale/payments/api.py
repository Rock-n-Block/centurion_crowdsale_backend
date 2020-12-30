from centurion_crowdsale.payments.models import Payment
from centurion_crowdsale.invest_requests.models import InvestRequest
from centurion_crowdsale.vouchers.models import Voucher
from centurion_crowdsale.rates.models import UsdRate
from centurion_crowdsale.consts import DECIMALS
from centurion_crowdsale.settings import USD_MINIMAL_PURCHASE_BIAS
import decimal
import traceback
import sys


def create_voucher(payment):
    try:
        rate_obj = UsdRate.objects.first()
    except UsdRate.DoesNotExist:
        raise Exception('CREATING VOUCHER ERROR: you should run rates_checker.py at least once')

    usd_rate = getattr(rate_obj, payment.currency)
    usd_amount = payment.amount / DECIMALS[payment.currency] / usd_rate

    project = payment.invest_request.project
    if usd_amount < project.usd_minimal_purchase:
        if usd_amount + USD_MINIMAL_PURCHASE_BIAS < project.usd_minimal_purchase:
            print(f'CREATING VOUCHER: minimal purchase is {project.usd_minimal_purchase}$ '
                  f'but {usd_amount}$ was received, voucher not created', flush=True)
            return None
        else:
            usd_amount = project.usd_minimal_purchase

    voucher = Voucher(
        project=project,
        payment=payment,
        usd_amount=decimal.Decimal(f'{usd_amount:.{2}f}'),
        email=payment.invest_request.email,
    )
    voucher.save()
    print(f'SAVING VOUCHER: {voucher.email}`s {voucher.project.project_name} voucher '
          f'for {voucher.usd_amount}$ successfully saved', flush=True)
    return voucher


def save_payment(invest_request, message):
    payment = Payment(
        invest_request=invest_request,
        currency=message['currency'],
        amount=message['amount'],
        tx_hash=message['transactionHash'],
    )
    payment.save()
    return payment


def parse_payment_message(message):
    tx_hash = message['transactionHash']
    if not Payment.objects.filter(tx_hash=tx_hash).count() > 0:
        invest_request = InvestRequest.objects.get(id=message['exchangeId'])
        project = invest_request.project
        payment = save_payment(invest_request, message)
        print(f'PARSING PAYMENT: {project.project_name} payment {payment.tx_hash} '
              f'for {payment.amount / DECIMALS[payment.currency]} {payment.currency} successfully saved', flush=True)

        voucher = create_voucher(payment)
        if voucher:
            if payment.currency == 'DUC':
                project.duc_collected += payment.amount / DECIMALS['DUC']
                project.usd_collected_from_duc += voucher.usd_amount
            else:
                project.usd_collected_from_fiat += voucher.usd_amount
            project.save()

            try:
                voucher.send_mail()
                print(f'SENDING VOUCHER: {voucher.project.project_name} voucher '
                      f'for {voucher.usd_amount}$ was successfully sent to {voucher.email}', flush=True)
                voucher.save()
            except Exception:
                print(f'SENDING VOUCHER ERROR: sending {voucher.project.project_name} voucher '
                      f'for {voucher.usd_amount}$ to {voucher.email} failed, error log: ', flush=True)
                print('\n'.join(traceback.format_exception(*sys.exc_info())), flush=True)
    else:
        print('PARSING PAYMENT: payment {tx_hash} already registered', flush=True)
