# environments = [
#     {
#         "id": "abc",
#         "size": "60x20x10",
#         "material": "stone",
#         "items": [
#             {
#                 "item_id": "necklace-x3e1",
#                 "size": "4x4in",
#             },
#             {
#                 "item_id": "ring-r4r3",
#                 "size": "1x1in",
#             },
#         ],
#     },
#     {
#         "id": "def",
#         "size": "20x20x20",
#         "material": "marble",
#         "items": [
#             {
#                 "item_id": "sword-z2z6",
#                 "size": "1x36in",
#             },
#         ],
#     },
#     {
#         "id": "ghi",
#         "size": "20x20x20",
#         "material": "quilt",
#         "items": [
#             {
#                 "item_id": "ball-555s",
#                 "size": "2x2in",
#             },
#         ],
#     },
# ]

from game_engine.api.map_inspector import MapInspector
from byo_network_hub.models import GameMap, GameState


def get_environment(environment_id, user_id):
    map_id = GameState.objects.get(user_id=user_id).map_id
    map = GameMap.objects.get(id=map_id).map_graph

    map_inspector = MapInspector(map)

    environment = map_inspector.get_env_by_id(environment_id)

    return environment
