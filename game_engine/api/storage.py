from byo_network_hub.models import GameMap, GameState, GameElementLookup, GameInventory
from game_engine.api.map_inspector import MapInspector


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

    GameInventory.objects.create(user_id=user_id, item_id=item_id, item_details=item)
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
