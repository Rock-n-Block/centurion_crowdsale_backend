import time
from centurion_crowdsale.transfers.api import transfer_ducx
from centurion_crowdsale.settings import DUCX_STAKING_TIMEOUT, DUCX_DECIMALS
from centurion_crowdsale.transfers.models import Transfer
from centurion_crowdsale.projects.models import CenturionProject
from centurion_crowdsale.rates.models import UsdRate
from celery import shared_task


@shared_task
def ducx_staking(project_id):
    project = CenturionProject.objects.get(string_id=project_id)
    token = project.token
    balances = token.holders_balances()
    token_decimals = 10 ** token.decimals
    k = project.ducx_staking_monthly_percent / 100
    print(f'DUCX STAKING: start {project.project_name} staking...', flush=True)
    errors = 0
    for address, balance in balances.items():
        ducx_rate = UsdRate.objects.first().DUCX
        amount = int(balance * k * ducx_rate * DUCX_DECIMALS / token_decimals)

        transfer = Transfer(
            amount=amount,
            currency='DUCX',
            ducx_address=address,
        )
        try:
            transfer.tx_hash = transfer_ducx(address, amount)
            transfer.status = 'WAITING FOR CONFIRM'
            print(f'DUCX STAKING: successful transfer {transfer.tx_hash} to {transfer.ducx_address} '
                  f'for {amount} DUCX', flush=True)
        except Exception as e:
            transfer.tx_error = repr(e)
            transfer.status = 'FAIL'

            print(f'DUCX STAKING: failed transfer {amount} DUCX to {transfer.ducx_address} '
                  f'with exception {transfer.tx_error}', flush=True)
            errors += 1
        transfer.save()
        time.sleep(DUCX_STAKING_TIMEOUT)
    print(f'DUCX STAKING: {project.project_name} staking completed with {errors} errors', flush=True)

