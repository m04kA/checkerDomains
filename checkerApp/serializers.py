from rest_framework import serializers


class VisitedLinksSerializer(serializers.Serializer):
    links = serializers.ListSerializer(child=serializers.URLField(), required=True)
