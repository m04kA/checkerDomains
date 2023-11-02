import datetime
import logging

from rest_framework import serializers

from checkerApp.models import UserDomainsHistory

logger = logging.getLogger(__name__)


class VisitedLinksSerializer(serializers.Serializer):
    links = serializers.ListSerializer(child=serializers.URLField(), required=True)
    user_id = serializers.SerializerMetaclass


class ViewPeriodSerializer(serializers.Serializer):
    start = serializers.IntegerField()
    finish = serializers.IntegerField()

    def validate(self, data):
        """
            Check that start is before finish.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError('start period more than finish')
        if data['start'] < 0:
            raise serializers.ValidationError('start period should be more 0')
        if data['finish'] < 0:
            raise serializers.ValidationError('start period should be more 0')
        return data


class DomainsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDomainsHistory
        fields = ('user_id', 'domain', 'created_at',)
