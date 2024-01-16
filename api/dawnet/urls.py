'''Endpoints for dawnet'''
from django.urls import include, path

from api.urls import OptionalSlashRouter

from .views import DAWNetView

from .views_byoc_ws_health_check import HealthCheckView
from .views_connect import Connect
from .views_byoc_compute_contract import ComputeContractListCreateView, ComputeContractRetrieveUpdateDestroyView
from .views_byoc_messages import SendMessageView, GetMessageResponseView, AbortMessagesView, ReplyToMessageView, \
    GetLatestPendingMessagesView, UpdateMessageStatusView
from .views_byoc_storage import SignedURLAPIView

router = OptionalSlashRouter()
router.register(r'dawnet', DAWNetView, basename='dawnet')
# router.register(r'healthcheck', HealthCheckView, basename='healthcheck')

post_dawnet_non_generic = DAWNetView.as_view({'post': 'post_dawnet_non_generic'})

urlpatterns = [
    path('dawnet/non-generic',
         post_dawnet_non_generic, name='post-dawnet-non-generic'),

    # DAWNet HEALTH CHECK
    path('hub/healthcheck/', HealthCheckView.as_view(), name='health-check'),

    # DAWNet CONNECTION
    path('hub/connection/compute/<str:token>/<int:connection_status>/', Connect.as_view(), name='connection/compute'),
    path('hub/connection/plugin/<str:token>/<int:connection_status>/', Connect.as_view(), name='connection/plugin'),
    path('hub/connections/', Connect.as_view(), name='connection-all'),
    path('hub/connections/<str:id>/', Connect.as_view(), name='connection'),

    # DAWNet COMPUTE CONTRACTS
    path('hub/compute/contract/', ComputeContractListCreateView.as_view(), name='compute-contract-list-create'),
    path('hub/compute/contract/<uuid:id>/', ComputeContractRetrieveUpdateDestroyView.as_view(),
         name='compute-contract-detail'),

    path('hub/send_message/', SendMessageView.as_view(), name='send-message'),
    path('hub/get_response/<uuid:id>/<str:token>/', GetMessageResponseView.as_view(), name='get-response'),
    path('hub/abort_messages/<str:token>/', AbortMessagesView.as_view(), name='abort-messages'),
    path('hub/reply_to_message/', ReplyToMessageView.as_view(), name='reply-to-message'),
    path('hub/get_latest_pending_messages/', GetLatestPendingMessagesView.as_view(),
         name='get-latest-pending-messages'),
    path(
        'api/hub/update_message_status/<str:token>/<uuid:message_id>/',
        UpdateMessageStatusView.as_view(),
        name='update-message-status'
    ),

    path('api/hub/get_signed_url/', SignedURLAPIView.as_view(), name='get-signed-url'),

    path('', include(router.urls)),
]
