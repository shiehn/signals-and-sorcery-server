"""DAWNet data validators"""
from rest_framework import serializers
from byo_network_hub.models import Connection


# pylint: disable=abstract-method
class DAWNetNonGenericSerializer(serializers.Serializer):
    """Used by the non generic call"""

    test = serializers.CharField(required=True, max_length=30, min_length=1)


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = "__all__"
