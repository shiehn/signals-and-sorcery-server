from byo_network_hub.models import (
    GameMap,
    GameMapState,
    GameState,
    GameElementLookup,
    GameInventory,
)
from game_engine.api.map_inspector import MapInspector
from game_engine.api.event_publisher import EventPublisher


def add_item(item_id: str):
    user_id = GameElementLookup.objects.get(element_id=item_id).user_id

    game_state = GameState.objects.get(user_id=user_id)

    current_env_id = game_state.environment_id

    map_id = game_state.map_id

    map = GameMap.objects.get(id=map_id).map_graph

    map_inspector = MapInspector(map)

    items = map_inspector.get_items_by_env_id(str(current_env_id))

    item = None
    for i in items:
        if i["item_id"] == item_id:
            item = i
            break

    if item is None:
        return False

    GameInventory.objects.create(
        user_id=user_id, item_id=item_id, map_id=map_id, item_details=item
    )

    game_state_item = GameMapState.objects.filter(
        map_id=map_id, item_id=item_id
    ).first()
    if game_state_item is None:
        new_game_state_item = GameMapState.objects.create(
            map_id=map_id, item_id=item_id, consumed=True
        )
        new_game_state_item.save()

    EventPublisher().publish_sync(user_id, "inventory-update")

    return True


def remove_item(item_id):
    # for i, item in enumerate(storage):
    #     if item["item_id"] == item_id:
    #         storage.pop(i)
    #         return True
    return False


def list_items(user_id: str):
    items = GameInventory.objects.filter(user_id=user_id)
    if items:
        return items

    return []
