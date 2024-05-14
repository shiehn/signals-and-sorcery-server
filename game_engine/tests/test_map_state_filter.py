import unittest
from unittest.mock import Mock
from game_engine.api.map_state_filter import MapStateFilter
from game_engine.api.map_inspector import MapInspector

import os
import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
# django.setup()


class TestGameMapInspector(unittest.TestCase):
    def test_map_state_filter(self):
        test_map = {
            "edges": [],
            "nodes": [
                {
                    "id": "6b9c7139-7991-4eb3-800e-3b2af4c6ffe8",
                    "color": {"background": "green"},
                    "label": "Entrance",
                    "shape": "box",
                    "game_info": {
                        "doors": [],
                        "items": [
                            {
                                "item_id": "06bbd11e-5d13-4fe8-aac2-c5bca9828b08",
                                "item_size": "4x6",
                                "item_type": "weapon",
                            },
                            {
                                "item_id": "36bbd11e-4d13-3fe8-aac2-d5bca9828b08",
                                "item_size": "4x6",
                                "item_type": "armor",
                            },
                        ],
                        "encounters": [
                            {
                                "encounter_id": "616f8262-0540-43d2-9925-3c9cc7989437",
                                "encounter_size": "6x6",
                                "encounter_type": "monster",
                            }
                        ],
                    },
                },
            ],
        }

        map_inspector = MapInspector(test_map)
        items = map_inspector.get_items_by_env_id(
            "6b9c7139-7991-4eb3-800e-3b2af4c6ffe8"
        )
        self.assertEqual(len(items), 2)

        map_inspector = MapInspector(test_map)
        encounters = map_inspector.get_encounters_by_env_id(
            "6b9c7139-7991-4eb3-800e-3b2af4c6ffe8"
        )
        self.assertEqual(
            encounters[0]["encounter_id"], "616f8262-0540-43d2-9925-3c9cc7989437"
        )

        map_state = [
            Mock(item_id="06bbd11e-5d13-4fe8-aac2-c5bca9828b08", consumed=True),
            Mock(item_id="36bbd11e-4d13-3fe8-aac2-d5bca9828b08", consumed=False),
            Mock(item_id="616f8262-0540-43d2-9925-3c9cc7989437", consumed=True),
        ]

        map_state_filter = MapStateFilter(test_map)
        filtered_map = map_state_filter.filter(map_state)

        map_inspector = MapInspector(filtered_map)
        items = map_inspector.get_items_by_env_id(
            "6b9c7139-7991-4eb3-800e-3b2af4c6ffe8"
        )
        self.assertEqual(len(items), 1)

        map_inspector = MapInspector(filtered_map)
        encounters = map_inspector.get_encounters_by_env_id(
            "6b9c7139-7991-4eb3-800e-3b2af4c6ffe8"
        )
        self.assertEqual(len(encounters), 0)
