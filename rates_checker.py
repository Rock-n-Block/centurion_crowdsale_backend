import os
import sys
import time
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'centurion_crowdsale.settings')
import django
django.setup()
from centurion_crowdsale.rates.models import UsdRate
from centurion_crowdsale.settings import RATES_CHECKER_TIMEOUT


if __name__ == '__main__':
    while True:
        rate = UsdRate.objects.first() or UsdRate()
        try:
            rate.update_rates()
            rate.save()
        except Exception as e:
            print('\n'.join(traceback.format_exception(*sys.exc_info())), flush=True)
            time.sleep(RATES_CHECKER_TIMEOUT)
            continue
        print('Saved ok!', flush=True)
        # print('new usd prices', usd_prices, flush=True)
        time.sleep(RATES_CHECKER_TIMEOUT)
