from rest_framework import serializers
from centurion_crowdsale.projects.models import CenturionProject
from centurion_crowdsale.ducx_tokens.models import DucxToken
from centurion_crowdsale.ducx_tokens.serializers import DucxTokenSerializer


class CenturionProjectSerializer(serializers.ModelSerializer):
    token = DucxTokenSerializer()
    raise_start_datetime = serializers.DateTimeField(format="%s", allow_null=True, required=False)
    raise_finish_datetime = serializers.DateTimeField(format="%s", read_only=True)

    class Meta:
        model = CenturionProject
        extra_kwargs = {
            'usd_collected_from_fiat': {'read_only': True},
            'usd_collected_from_duc': {'read_only': True},
            'duc_collected': {'read_only': True},
        }
        fields = (
            'token',
            'string_id',
            'category',
            'status',
            'project_name',
            'description',
            'description_title',
            'default_image',
            'images',
            'investors',
            'raise_start_datetime',
            'raise_months',
            'raise_finish_datetime',
            'months_between_raise_and_staking',
            'staking_months',
            'ducx_staking_monthly_percent',
            'ducx_staking_total_percent',
            'duc_percent_in_target_raise',
            'fiat_percent_in_target_raise',
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

    def create(self, validated_data):
        token_validated_data = validated_data['token']
        token = DucxToken.objects.create(**token_validated_data)
        validated_data['token'] = token
        project = CenturionProject.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        token_validated_data = validated_data.pop('token')
        token = instance.token
        for attr, value in token_validated_data.items():
            setattr(token, attr, value)
        token.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
