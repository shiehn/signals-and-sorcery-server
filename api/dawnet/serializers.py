"""DAWNet data validators"""

from rest_framework import serializers
from byo_network_hub.models import (
    Connection,
    RemoteImage,
    RemoteSource,
    GameMap,
    GameMapState,
    GameState,
    GameInventory,
    GameUpdateQueue,
)


# pylint: disable=abstract-method
class DAWNetNonGenericSerializer(serializers.Serializer):
    """Used by the non generic call"""

    test = serializers.CharField(required=True, max_length=30, min_length=1)


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = "__all__"


class RemoteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteImage
        fields = "__all__"


class RemoteSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteSource
        fields = "__all__"


# GAME MAP MODELS -----------------------------------------------


class GameStateSerializer(serializers.ModelSerializer):
    environment_id = serializers.UUIDField(required=False, allow_null=True)
    environment_img = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = GameState
        fields = [
            "map_id",
            "level",
            "created_at",
            "updated_at",
            "aesthetic",
            "art_style",
            "setting",
            "environment_id",
            "environment_img",
        ]
        extra_kwargs = {
            "map_id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        # User is added in the view's perform_create method, not here
        return super().create(validated_data)


class GameMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMap
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class GameMapStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMapState
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class GameInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameInventory
        fields = [
            "id",
            "user_id",
            "map_id",
            "item_id",
            "item_details",
            "created_at",
            "updated_at",
        ]


class GameUpdateQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUpdateQueue
        fields = ["user_id", "level", "status"]
