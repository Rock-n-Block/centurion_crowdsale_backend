from rest_framework import serializers
from centurion_crowdsale.projects.models import CenturionProject


class CenturionProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenturionProject
        extra_kwargs = {
            'id': {'read_only': True},
            'usd_collected_from_fiat': {'read_only': True},
            'usd_collected_from_duc': {'read_only': True},
            'duc_collected': {'read_only': True}
        }
        fields = (
            'id',
            'category',
            'status',
            'project_name',
            'description',
            'images',
            'investors',
            'raise_start_date',
            'raise_months',
            'raise_finish_date',
            'months_between_raise_and_staking',
            'staking_months',
            'ducx_staking_monthly_percent',
            'ducx_staking_total_percent',
            'duc_percent_in_target_raise',
            'usd_target_raise',
            'usd_minimal_purchase',
            'usd_collected_from_fiat',
            'usd_collected_from_duc',
            'usd_collected',
            'duc_collected',
            'usd_from_fiat_target_raise',
            'usd_from_duc_target_raise',
            'duc_target_raise',
        )


class CenturionProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenturionProject
        fields = (
            'id',
            'default_image',
            'project_name',
            'description',
            'raise_finish_date',
            'usd_collected',
            'usd_target_raise'
        )
