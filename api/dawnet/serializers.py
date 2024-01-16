'''DAWNet data validators'''
from rest_framework import serializers




# pylint: disable=abstract-method
class DAWNetNonGenericSerializer(serializers.Serializer):
    '''Used by the non generic call'''
    test = serializers.CharField(required=True, max_length=30, min_length=1)


