from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from centurion_crowdsale.settings import DUC_RATE
from django.contrib.postgres.fields import ArrayField
from centurion_crowdsale.vouchers.models import Voucher


class CenturionProject(models.Model):
    token = models.OneToOneField('ducx_tokens.DucxToken', on_delete=models.CASCADE)
    string_id = models.CharField(max_length=50, unique=True, primary_key=True)
    category = models.CharField(max_length=20)
    project_name = models.CharField(max_length=50)
    description_title = models.CharField(max_length=50)
    description = models.TextField(default='')
    images = ArrayField(models.CharField(max_length=50), default=list)
    default_image = models.CharField(max_length=50)
    usd_target_raise = models.DecimalField(max_digits=100, decimal_places=2)
    usd_collected_from_fiat = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    usd_collected_from_duc = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    duc_collected = models.DecimalField(max_digits=100, decimal_places=0, default=0)
    usd_minimal_purchase = models.IntegerField()
    raise_start_datetime = models.DateTimeField(null=True, default=None)
    raise_months = models.IntegerField()
    months_between_raise_and_staking = models.IntegerField()
    duc_percent_in_target_raise = models.IntegerField()
    ducx_staking_monthly_percent = models.IntegerField()
    staking_months = models.IntegerField()

    @property
    def status(self):
        now = timezone.now()
        if self.raise_start_datetime is None or now < self.raise_start_datetime:
            return 'COMING SOON'
        elif now <= self.raise_finish_datetime:
            if self.usd_collected >= self.usd_target_raise:
                return 'COMPLETED'
            return 'ACTIVE'
        else:
            if self.usd_collected >= self.usd_target_raise:
                return 'COMPLETED'
            return 'EXPIRED'

    @property
    def raise_finish_datetime(self):
        if self.raise_start_datetime is None:
            return None
        return self.raise_start_datetime + relativedelta(months=self.raise_months)

    @property
    def staking_start_datetime(self):
        return self.raise_finish_datetime + relativedelta(months=self.months_between_raise_and_staking)

    @property
    def staking_finish_datetime(self):
        return self.raise_finish_datetime + \
               relativedelta(months=self.months_between_raise_and_staking + self.staking_months - 1)

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
