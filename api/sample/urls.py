'''Endpoints for sample'''
from django.urls import include, path

from api.urls import OptionalSlashRouter

from .views import SampleView

from .views_byoc_ws_health_check import HealthCheckView
from .views_connect import Connect


router = OptionalSlashRouter()
router.register(r'sample', SampleView, basename='sample')
#router.register(r'healthcheck', HealthCheckView, basename='healthcheck')

post_sample_non_generic = SampleView.as_view({'post': 'post_sample_non_generic'})

urlpatterns = [
    path('sample/non-generic',
         post_sample_non_generic, name='post-sample-non-generic'),


    path('hub/healthcheck/', HealthCheckView.as_view(), name='health-check'),

    path('hub/connection/compute/<str:token>/<int:connection_status>/', Connect.as_view(), name='connection/compute'),
    path('hub/connection/plugin/<str:token>/<int:connection_status>/', Connect.as_view(), name='connection/plugin'),
    path('hub/connections/', Connect.as_view(), name='connection-all'),
    path('hub/connections/<str:id>/', Connect.as_view(), name='connection'),


    path('', include(router.urls)),
]
