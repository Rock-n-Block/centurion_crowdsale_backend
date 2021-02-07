from django.contrib import admin
from centurion_crowdsale.projects.models import CenturionProject


class CenturionProjectAdmin(admin.ModelAdmin):
    readonly_fields = (
        'status',
        'investors',
        'raise_finish_datetime',
        'staking_start_datetime',
        'staking_finish_datetime',
        'duc_target_raise',
        'usd_from_fiat_target_raise',
        'usd_from_duc_target_raise',
        'fiat_percent_in_target_raise',
        'usd_collected',
        'duc_collected',
        'usd_collected_from_fiat',
        'usd_collected_from_duc',
        'ducx_staking_total_percent',
    )


admin.site.register(CenturionProject, CenturionProjectAdmin)
