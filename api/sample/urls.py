'''Endpoints for sample'''
from django.urls import include, path

from api.urls import OptionalSlashRouter

from .views import SampleView


router = OptionalSlashRouter()
router.register(r'sample', SampleView, basename='sample')

post_sample_non_generic = SampleView.as_view({'post': 'post_sample_non_generic'})

urlpatterns = [
    path('sample/non-generic',
         post_sample_non_generic, name='post-sample-non-generic'),
    path('', include(router.urls)),
]
