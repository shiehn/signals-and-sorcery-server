'''Sample logic for API'''
from django.utils.translation import gettext_lazy as _

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from api.utils.utils import serializer_errors_to_string
from api.utils.mixins import RequestLanguageMixin

from .serializers import SampleNonGenericSerializer


class SampleView(RequestLanguageMixin, viewsets.ViewSet):
    '''API view for Sample'''
    lookup_field = 'sample_id'

    # pylint: disable=no-self-use
    def list(self, request: Request) -> Response:
        '''
        GET /sample
        List all samples
        '''
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)

    # pylint: disable=invalid-name, no-self-use
    def retrieve(self, request: Request, sample_id: str = None) -> Response:
        '''
        GET /sample/<sample_id>
        Retrieve a specific sample
        '''
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)

    # pylint: disable=no-self-use
    def create(self, request: Request) -> Response:
        '''
        POST /sample
        Create a sample
        '''
        return Response({'message': _('Success')}, status=status.HTTP_201_CREATED)

    # pylint: disable=invalid-name, no-self-use
    def update(self, request: Request, sample_id: str = None) -> Response:
        '''
        PUT /sample/<sample_id>
        Update a sample
        '''
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)

    # pylint: disable=invalid-name, no-self-use
    def destroy(self, request: Request, sample_id: str = None) -> Response:
        '''
        DELETE /sample/<sample_id>
        Delete a sample
        '''
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)

    # pylint: disable=no-self-use
    def post_sample_non_generic(self, request: Request) -> Response:
        '''
        POST /sample/non-generic
        Sample non generic view
        '''
        # Access the language got from the mixins RequestLanguageMixin
        print(request.lang)

        # Check the data validity
        serializer = SampleNonGenericSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response({
                'message': serializer_errors_to_string(serializer.errors)},
                status=status.HTTP_400_BAD_REQUEST)

        # Get the data from serializer
        data = serializer.validated_data
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)
