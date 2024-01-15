'''A group of mixins used in the API vies'''
from rest_framework.request import Request
from rest_framework.response import Response

from common.helper import get_languages_array


# pylint: disable=too-few-public-methods
class RequestLanguageMixin:
    '''Mixin to handle language'''

    def dispatch(self, request: Request, *args, **kwargs) -> Response:
        '''Get the language and save into the request'''
        # If the language is not in the handled languages, we set it as default
        request.lang = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if request.lang not in get_languages_array():
            request.lang = 'fr'

        return super().dispatch(request, *args, **kwargs)
