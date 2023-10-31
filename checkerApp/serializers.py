from rest_framework import serializers


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
        return data
