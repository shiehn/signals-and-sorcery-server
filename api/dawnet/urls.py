"""Endpoints for dawnet"""

from django.urls import include, path

from api.urls import OptionalSlashRouter

from .views import DAWNetView

from .views_byoc_ws_health_check import HealthCheckView
from .views_connect import Connect, UpdateLoadedStatus
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
from .views_game_engine import GameQueryView
from .views_game_engine_map import GameMapView, GameMapCreateView
from .views_game_engine_map_state import GameMapStateViewSet
from .views_game_engine_map_generation import GameMapGeneration
from . import views_connections
from .views_connection_expiration import ConnectionsTimeout
from .views_connection_cleanup import ConnectionsCleanUp
from .views_game_engine_state import (
    GameStateDetailView,
    GameStateDeleteView,
    GameStateUpdateView,
    GameStateCreateView,
)


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
    path(
        "hub/connections/<str:connection_token>/loaded/",
        UpdateLoadedStatus.as_view(),
        name="connection-loaded-update",
    ),
    path(
        "hub/connections_timeout/",
        ConnectionsTimeout.as_view(),
        name="connections-timeout",
    ),
    path(
        "hub/connections_expiry/",
        ConnectionsCleanUp.as_view(),
        name="connections-cleanup",
    ),
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
        "hub/get_latest_pending_messages/<uuid:connection_token>/",
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
    path(
        "game-engine/query/",
        GameQueryView.as_view(),
        name="handle-user-query",
    ),
    path("game-map/<uuid:uuid>/", GameMapView.as_view(), name="game-map"),
    path("game-map/", GameMapCreateView.as_view(), name="create-game-map"),
    path(
        "game-map-states/",
        GameMapStateViewSet.as_view({"get": "list", "post": "create"}),
        name="game-map-states",
    ),
    path(
        "game-map-generation/", GameMapGeneration.as_view(), name="game-map-generation"
    ),
    path("game-state/", GameStateCreateView.as_view(), name="game-state-create"),
    path(
        "game-state/<uuid:user_id>/",
        GameStateDetailView.as_view(),
        name="game-state-detail",
    ),
    path(
        "game-state/<uuid:id>/delete/",
        GameStateDeleteView.as_view(),
        name="game-state-delete",
    ),
    path(
        "game-state/<uuid:id>/update/",
        GameStateUpdateView.as_view(),
        name="game-state-update",
    ),
    path("", include(router.urls)),
]
