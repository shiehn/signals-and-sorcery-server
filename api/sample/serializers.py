'''Sample data validators'''
from rest_framework import serializers




# pylint: disable=abstract-method
class SampleNonGenericSerializer(serializers.Serializer):
    '''Used by the non generic call'''
    test = serializers.CharField(required=True, max_length=30, min_length=1)


