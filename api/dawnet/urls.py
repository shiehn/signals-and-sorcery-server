"""Endpoints for dawnet"""

from django.urls import include, path

from api.urls import OptionalSlashRouter

from .views import DAWNetView

from .views_byoc_ws_health_check import HealthCheckView
from .views_connect import Connect
from .views_byoc_compute_contract import (
    ComputeContractListCreateView,
    ComputeContractRetrieveUpdateDestroyView,
)
from .views_byoc_messages import (
    SendMessageView,
    GetMessageResponseView,
    AbortMessagesView,
    ReplyToMessageView,
    GetLatestPendingMessagesView,
    UpdateMessageStatusView,
)
from .views_byoc_storage import SignedURLAPIView
from .views_remote_images import RemoteImageListView, RemoteImageDeleteView
from .views_remote_sources import RemoteSourceListView, RemoteSourceDeleteView
from . import views_connections

router = OptionalSlashRouter()
# router.register(r"dawnet", DAWNetView, basename="dawnet")
# router.register(r'healthcheck', HealthCheckView, basename='healthcheck')

# post_dawnet_non_generic = DAWNetView.as_view({"post": "post_dawnet_non_generic"})

urlpatterns = [
    # path("dawnet/non-generic", post_dawnet_non_generic, name="post-dawnet-non-generic"),
    # DAWNet HEALTH CHECK
    path("hub/healthcheck/", HealthCheckView.as_view(), name="health-check"),
    # DAWNet CONNECTION
    path(
        "hub/connection/compute/<str:token>/<int:connection_status>/",
        Connect.as_view(),
        name="connection/compute",
    ),
    path(
        "hub/connection/plugin/<str:token>/<int:connection_status>/",
        Connect.as_view(),
        name="connection/plugin",
    ),
    path("hub/connections/", Connect.as_view(), name="connection-all"),
    path("hub/connections/<str:id>/", Connect.as_view(), name="connection"),
    # DAWNet COMPUTE CONTRACTS
    path(
        "hub/compute/contract/",
        ComputeContractListCreateView.as_view(),
        name="compute-contract-list-create",
    ),
    path(
        "hub/compute/contract/<uuid:id>/",
        ComputeContractRetrieveUpdateDestroyView.as_view(),
        name="compute-contract-detail",
    ),
    path("hub/send_message/", SendMessageView.as_view(), name="send-message"),
    path(
        "hub/get_response/<uuid:id>/<str:token>/",
        GetMessageResponseView.as_view(),
        name="get-response",
    ),
    path(
        "hub/abort_messages/<str:token>/",
        AbortMessagesView.as_view(),
        name="abort-messages",
    ),
    path(
        "hub/reply_to_message/", ReplyToMessageView.as_view(), name="reply-to-message"
    ),
    path(
        "hub/get_latest_pending_messages/",
        GetLatestPendingMessagesView.as_view(),
        name="get-latest-pending-messages",
    ),
    path(
        "hub/update_message_status/<str:token>/<uuid:message_id>/",
        UpdateMessageStatusView.as_view(),
        name="update-message-status",
    ),
    path("hub/get_signed_url/", SignedURLAPIView.as_view(), name="get-signed-url"),
    # CONNECTION MAPPING (Master Token <-> Connection Token)
    path(
        "hub/connection_mappings/",
        views_connections.ConnectionListCreateView.as_view(),
        name="connection-list-create",
    ),
    path(
        "hub/connection_mappings/<uuid:master_token>/",
        views_connections.ConnectionListByMasterTokenView.as_view(),
        name="connection-list-by-master-token",
    ),
    path(
        "hub/connection_mappings/<uuid:master_token>/<uuid:connection_token>/",
        views_connections.ConnectionDetailView.as_view(),
        name="connection-detail",
    ),
    path("hub/remote-images/", RemoteImageListView.as_view(), name="remote-image-list"),
    path(
        "hub/remote-images/<str:id>/",
        RemoteImageDeleteView.as_view(),
        name="remote-image-delete",
    ),
    path(
        "hub/remote-sources/", RemoteSourceListView.as_view(), name="remote-source-list"
    ),
    path(
        "hub/remote-sources/<str:id>/",
        RemoteSourceDeleteView.as_view(),
        name="remote-source-delete",
    ),
    path("", include(router.urls)),
]
