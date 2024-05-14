import unittest
from game_engine.api.map_generator import MapGenerator
from game_engine.api.map_processor import MapProcessor
from game_engine.api.map_inspector import MapInspector

# python manage.py test game_engine.tests.test_generator


class TestGameMapInspector(unittest.TestCase):
    def test_get_environment_id_of_entrance(self):
        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=3, percent_connected=0.25
        ).get_json()

        map_processor = MapProcessor(unprocessed_map)
        map_processor = map_processor.add_entrance_exit()
        map_processor = map_processor.add_items()

        map = map_processor.get_map()

        map_inspector = MapInspector(map)
        entrance_id = map_inspector.get_env_id_of_entrance()

        self.assertIsNotNone(entrance_id)

    def test_get_environment_id_of_exit(self):
        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=3, percent_connected=0.25
        ).get_json()

        map_processor = MapProcessor(unprocessed_map)
        map_processor = map_processor.add_entrance_exit()
        map_processor = map_processor.add_items()

        map = map_processor.get_map()

        map_inspector = MapInspector(map)
        exit_id = map_inspector.get_env_id_of_exit()

        self.assertIsNotNone(exit_id)

    def test_get_element_ids(self):
        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=3, percent_connected=0.25
        ).get_json()

        map_processor = MapProcessor(unprocessed_map)
        map_processor = map_processor.add_entrance_exit()
        map_processor = map_processor.add_items()
        map_processor = map_processor.add_encounters()

        map = map_processor.get_map()

        map_inspector = MapInspector(map)

        uuids = map_inspector.extract_uuids()

        print(str(uuids))

        self.assertGreater(len(uuids), 4)

    def test_get_adjacent_environments(self):
        test_map = {
            "edges": [
                {
                    "to": "82095dcb-542c-4621-8fd5-570e0b10d6e7",
                    "from": "71152afc-0b0d-452e-bb76-10fe44037fb7",
                },
                {
                    "from": "82095dcb-542c-4621-8fd5-570e0b10d6e7",
                    "to": "6b9c7139-7991-4eb3-800e-3b2af4c6ffe8",
                },
            ],
            "nodes": [
                {
                    "id": "71152afc-0b0d-452e-bb76-10fe44037fb7",
                    "color": {"background": "red"},
                    "label": "Exit",
                    "shape": "box",
                    "game_info": {
                        "doors": [],
                        "items": [
                            {
                                "item_id": "9ce263d4-8ad1-4464-81ce-9bd5eb97fa08",
                                "item_size": "4x6",
                                "item_type": "weapon",
                            },
                            {
                                "item_id": "b2540f46-06ec-403d-a593-0b197829481f",
                                "item_size": "4x6",
                                "item_type": "potion",
                            },
                        ],
                        "encounters": [],
                    },
                },
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
                            }
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
                {
                    "id": "82095dcb-542c-4621-8fd5-570e0b10d6e7",
                    "label": "820",
                    "shape": "box",
                    "game_info": {
                        "doors": [],
                        "items": [
                            {
                                "item_id": "cd5d0680-b9c3-4b99-8fa0-c40870c898c9",
                                "item_size": "4x6",
                                "item_type": "potion",
                            },
                            {
                                "item_id": "48a31ea3-a708-4cc1-aa73-78458b12c856",
                                "item_size": "4x6",
                                "item_type": "armor",
                            },
                        ],
                        "encounters": [
                            {
                                "encounter_id": "1a8bcff2-86cf-47d2-a582-dec69079e354",
                                "encounter_size": "6x6",
                                "encounter_type": "monster",
                            }
                        ],
                    },
                },
            ],
        }

        map_inspector = MapInspector(test_map)

        adjacent_envs = map_inspector.get_adjacent_environments(
            "82095dcb-542c-4621-8fd5-570e0b10d6e7"
        )

        self.assertEqual(len(adjacent_envs), 2)

    def test_get_adjacent_environments_one_result(self):
        map = {
            "edges": [
                {
                    "to": "92d3e1d7-8f65-4271-b105-3d653b86f0cc",
                    "from": "37ea742e-1693-4001-be17-2f9c90b22f03",
                },
                {
                    "to": "f0dc650f-b555-4ff8-8435-852e239de974",
                    "from": "37ea742e-1693-4001-be17-2f9c90b22f03",
                },
            ],
            "nodes": [
                {
                    "id": "37ea742e-1693-4001-be17-2f9c90b22f03",
                    "label": "37e",
                    "shape": "box",
                    "game_info": {"doors": [], "items": [], "encounters": []},
                },
                {
                    "id": "92d3e1d7-8f65-4271-b105-3d653b86f0cc",
                    "color": {"background": "red"},
                    "label": "Exit",
                    "shape": "box",
                    "game_info": {"doors": [], "items": [], "encounters": []},
                },
                {
                    "id": "f0dc650f-b555-4ff8-8435-852e239de974",
                    "color": {"background": "green"},
                    "label": "Entrance",
                    "shape": "box",
                    "game_info": {"doors": [], "items": [], "encounters": []},
                },
            ],
        }

        map_inspector = MapInspector(map)

        adjacent_envs = map_inspector.get_adjacent_environments(
            "f0dc650f-b555-4ff8-8435-852e239de974"
        )

        self.assertEqual(len(adjacent_envs), 1)

    def test_get_environment_by_id(self):
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

        env = map_inspector.get_env_by_id("6b9c7139-7991-4eb3-800e-3b2af4c6ffe8")

        self.assertEqual(len(env["game_info"]["items"]), 2)
