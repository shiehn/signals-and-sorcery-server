'''DAWNet logic for API'''
from django.utils.translation import gettext_lazy as _

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from api.utils.utils import serializer_errors_to_string
from api.utils.mixins import RequestLanguageMixin

from .serializers import DAWNetNonGenericSerializer


class DAWNetView(RequestLanguageMixin, viewsets.ViewSet):
    '''API view for DAWNet'''
    lookup_field = 'dawnet_id'

    # pylint: disable=no-self-use
    def list(self, request: Request) -> Response:
        '''
        GET /dawnet
        List all dawnet
        '''
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)

    # pylint: disable=invalid-name, no-self-use
    def retrieve(self, request: Request, dawnet_id: str = None) -> Response:
        '''
        GET /dawnet/<dawnet_id>
        Retrieve a specific dawnet
        '''
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)

    # pylint: disable=no-self-use
    def create(self, request: Request) -> Response:
        '''
        POST /dawnet
        Create a dawnet
        '''
        return Response({'message': _('Success')}, status=status.HTTP_201_CREATED)

    # pylint: disable=invalid-name, no-self-use
    def update(self, request: Request, dawnet_id: str = None) -> Response:
        '''
        PUT /dawnet/<dawnet_id>
        Update a dawnet
        '''
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)

    # pylint: disable=invalid-name, no-self-use
    def destroy(self, request: Request, dawnet_id: str = None) -> Response:
        '''
        DELETE /dawnet/<dawnet_id>
        Delete a dawnet
        '''
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)

    # pylint: disable=no-self-use
    def post_dawnet_non_generic(self, request: Request) -> Response:
        '''
        POST /dawnet/non-generic
        DAWNet non generic view
        '''
        # Access the language got from the mixins RequestLanguageMixin
        print(request.lang)

        # Check the data validity
        serializer = DAWNetNonGenericSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response({
                'message': serializer_errors_to_string(serializer.errors)},
                status=status.HTTP_400_BAD_REQUEST)

        # Get the data from serializer
        data = serializer.validated_data
        return Response({'message': _('Success')}, status=status.HTTP_200_OK)
