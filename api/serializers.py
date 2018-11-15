"""Serializers to map the Model instances into JSON format."""

from rest_framework import serializers
from iconviewer.models import Icon


class IconSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""

        model = Icon
        fields = ('uuid', 'name', 'get_tags', 'file', 'abs_path')
        read_only_fields = ('uuid', 'file', 'abs_path', 'get_tags')

