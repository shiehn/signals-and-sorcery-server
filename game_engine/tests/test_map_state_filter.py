import unittest
from unittest.mock import Mock
from game_engine.api.map_state_filter import MapStateFilter
from game_engine.api.map_inspector import MapInspector


class TestGameMapInspector(unittest.TestCase):
    def test_map_state_filter(self):
        test_map = {
            "edges": [
                {
                    "to": "e2b25d56-5c6d-4e9c-a744-362d09364f30",
                    "from": "16173b2f-c79e-4c90-8742-4e8108087893",
                },
                {
                    "to": "68a0936d-369e-435a-9788-ab7301575af3",
                    "from": "e2b25d56-5c6d-4e9c-a744-362d09364f30",
                },
                {
                    "to": "bb7b2036-0ce4-44eb-81af-7f05ba29bc27",
                    "from": "68a0936d-369e-435a-9788-ab7301575af3",
                },
            ],
            "nodes": [
                {
                    "id": "16173b2f-c79e-4c90-8742-4e8108087893",
                    "color": {"background": "gray"},
                    "label": "161",
                    "shape": "box",
                    "game_info": {
                        "doors": [],
                        "items": [],
                        "encounters": [],
                        "environment": {
                            "aesthetic": {
                                "image": "https://storage.googleapis.com/byoc-file-transfer/b15ba683-e4af-4be5-8ca6-4e0bd8435c31.png",
                                "description": "Imagine a watercolor painting...",
                            }
                        },
                    },
                },
                {
                    "id": "e2b25d56-5c6d-4e9c-a744-362d09364f30",
                    "color": {"background": "gray"},
                    "label": "e2b",
                    "shape": "box",
                    "game_info": {
                        "doors": [],
                        "items": [
                            {
                                "item_id": "08147572-c200-4fc2-a7c6-6f58d4c05d16",
                                "aesthetic": {
                                    "image": "https://storage.googleapis.com/byoc-file-transfer/fc7daa53-ec30-40e2-b11c-9dc7d30cfbe4.png",
                                    "description": "In the mystical realm of humanoid crows and pigeons...",
                                },
                                "item_type": "weapon",
                                "item_level": 65,
                            }
                        ],
                        "encounters": [
                            {
                                "aesthetic": {
                                    "image": "https://storage.googleapis.com/byoc-file-transfer/9fd33f36-9cc1-4a85-8a4a-c9ed64093981.png",
                                    "description": "In the misty realm of Aviara...",
                                },
                                "encounter_id": "f5ca4ae5-01a3-48bf-89a4-733cf2ed2831",
                                "encounter_type": "monster",
                                "encounter_level": 1,
                            }
                        ],
                        "environment": {
                            "aesthetic": {
                                "image": "https://storage.googleapis.com/byoc-file-transfer/2ecfa136-811a-41c5-856f-513d17edf05c.png",
                                "description": "In the vast and mystical world of Aviara...",
                            }
                        },
                    },
                },
                {
                    "id": "68a0936d-369e-435a-9788-ab7301575af3",
                    "color": {"background": "green"},
                    "label": "Entrance",
                    "shape": "box",
                    "game_info": {
                        "doors": [
                            "e2b25d56-5c6d-4e9c-a744-362d09364f30",
                            "bb7b2036-0ce4-44eb-81af-7f05ba29bc27",
                        ],
                        "items": [
                            {
                                "item_id": "7b58ffc3-260f-46df-9049-01328e08e5e6",
                                "aesthetic": {
                                    "image": "https://storage.googleapis.com/byoc-file-transfer/4ae17f39-b613-4592-9102-dee12d955c9f.png",
                                    "description": "In the ethereal realm of humanoid crows and pigeons...",
                                },
                                "item_type": "weapon",
                                "item_level": 55,
                            },
                            {
                                "item_id": "dc60d36d-054e-4465-a31d-0f75181505da",
                                "aesthetic": {
                                    "image": "https://storage.googleapis.com/byoc-file-transfer/631916df-1b44-4184-b030-2e32632415ba.png",
                                    "description": "In the mystical realm of Aviantasia...",
                                },
                                "item_type": "potion",
                                "item_level": 13,
                            },
                        ],
                        "encounters": [],
                        "environment": {
                            "aesthetic": {
                                "image": "https://storage.googleapis.com/byoc-file-transfer/a6595025-4929-4107-a2c4-7047dcef7cb4.png",
                                "description": "Welcome to the ethereal world of Aviaria...",
                            }
                        },
                    },
                },
                {
                    "id": "bb7b2036-0ce4-44eb-81af-7f05ba29bc27",
                    "color": {"background": "red"},
                    "label": "Exit",
                    "shape": "box",
                    "game_info": {
                        "doors": [],
                        "items": [
                            {
                                "item_id": "ac66b314-8492-415f-98ca-864f14c10f6f",
                                "aesthetic": {
                                    "image": "https://storage.googleapis.com/byoc-file-transfer/f0b184fe-e578-4447-9308-56edfeff5541.png",
                                    "description": "Behold the Enchanter's Elixir...",
                                },
                                "item_type": "potion",
                                "item_level": 15,
                            },
                            {
                                "item_id": "14625ea2-4b5e-4899-bf22-dc07f9754980",
                                "aesthetic": {
                                    "image": "https://storage.googleapis.com/byoc-file-transfer/9e41debd-e0e1-4616-94bb-bc896afd7961.png",
                                    "description": "Introducing the 'Feathered Serenade Elixir,' a potion inspired by the ethereal beauty of a world inhabited by humanoid crows and pigeons...",
                                },
                                "item_type": "potion",
                                "item_level": 34,
                            },
                        ],
                        "encounters": [],
                        "environment": {
                            "aesthetic": {
                                "image": "https://storage.googleapis.com/byoc-file-transfer/4a7c202e-dc22-425c-8c45-458aeb03b70c.png",
                                "description": "Welcome to the enchanting realm of Aviarra...",
                            }
                        },
                    },
                },
            ],
        }

        map_state = [
            Mock(item_id="f5ca4ae5-01a3-48bf-89a4-733cf2ed2831", consumed=True),
            Mock(item_id="08147572-c200-4fc2-a7c6-6f58d4c05d16", consumed=True),
            Mock(item_id="dc60d36d-054e-4465-a31d-0f75181505da", consumed=False),
        ]

        map_state_filter = MapStateFilter(test_map)
        filtered_map = map_state_filter.filter(map_state)

        # Assert that the filtered map no longer contains the consumed item and encounter
        for node in filtered_map["nodes"]:
            for item in node["game_info"].get("items", []):
                self.assertNotIn(
                    item["item_id"],
                    {
                        "f5ca4ae5-01a3-48bf-89a4-733cf2ed2831",
                        "08147572-c200-4fc2-a7c6-6f58d4c05d16",
                    },
                )

            for encounter in node["game_info"].get("encounters", []):
                self.assertNotIn(
                    encounter["encounter_id"], {"f5ca4ae5-01a3-48bf-89a4-733cf2ed2831"}
                )


if __name__ == "__main__":
    unittest.main()
