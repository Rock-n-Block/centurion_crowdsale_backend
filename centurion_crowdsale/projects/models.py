from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
from centurion_crowdsale.settings import DUC_RATE
from django.contrib.postgres.fields import ArrayField
from centurion_crowdsale.vouchers.models import Voucher


class CenturionProject(models.Model):
    category = models.CharField(max_length=20)
    project_name = models.CharField(max_length=50)
    string_id = models.CharField(max_length=50, unique=True)
    description_title = models.CharField(max_length=50)
    description = models.TextField(default='')
    images = ArrayField(models.CharField(max_length=50), default=list)
    default_image = models.CharField(max_length=50)
    usd_target_raise = models.DecimalField(max_digits=100, decimal_places=2)
    usd_collected_from_fiat = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    usd_collected_from_duc = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    duc_collected = models.DecimalField(max_digits=100, decimal_places=0, default=0)
    usd_minimal_purchase = models.IntegerField()
    raise_start_date = models.DateField(null=True, default=None)
    raise_months = models.IntegerField()
    months_between_raise_and_staking = models.IntegerField()
    duc_percent_in_target_raise = models.IntegerField()
    ducx_staking_monthly_percent = models.IntegerField()
    staking_months = models.IntegerField()

    @property
    def status(self):
        today = date.today()
        if not self.raise_start_date or today < self.raise_start_date:
            return 'COMING SOON'
        elif today <= self.raise_finish_date:
            return 'ACTIVE'
        elif today < self.raise_finish_date + relativedelta(months=self.months_between_raise_and_staking):
            return 'WAITING FOR STAKING'
        elif today < self.raise_finish_date + relativedelta(
                months=self.months_between_raise_and_staking + self.staking_months):
            return 'STAKING'
        return 'FINISHED'

    @property
    def raise_finish_date(self):
        return self.raise_start_date + relativedelta(months=self.raise_months) if self.raise_start_date else None

    @property
    def usd_collected(self):
        return self.usd_collected_from_fiat + self.usd_collected_from_duc

    @property
    def investors(self):
        return len(Voucher.objects.filter(project=self).values('email').distinct())

    @property
    def duc_target_raise(self):
        return float(self.usd_target_raise * self.duc_percent_in_target_raise) / (100 * DUC_RATE)

    @property
    def usd_from_fiat_target_raise(self):
        return self.usd_target_raise * (100 - self.duc_percent_in_target_raise) / 100

    @property
    def usd_from_duc_target_raise(self):
        return self.usd_target_raise * self.duc_percent_in_target_raise / 100

    @property
    def ducx_staking_total_percent(self):
        return self.staking_months * self.ducx_staking_monthly_percent

    @property
    def fiat_percent_in_target_raise(self):
        return 100 - self.duc_percent_in_target_raise
