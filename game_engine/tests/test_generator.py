import unittest
from game_engine.api.map_generator import MapGenerator
from game_engine.api.map_processor import MapProcessor

# python manage.py test game_engine.tests.test_generator


class TestCalculator(unittest.TestCase):
    def test_node_count(self):
        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=3, percent_connected=0.25
        ).get_json()

        self.assertEqual(len(unprocessed_map["nodes"]), 3)

        # processed_map = MapProcessor(unprocessed_map)
        # processed_map = processed_map.add_entrance_exit()

    def test_adding_enter_exit(self):
        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=3, percent_connected=0.25
        ).get_json()

        map_processor = MapProcessor(unprocessed_map)
        map_processor = map_processor.add_entrance_exit()
        map_processor = map_processor.add_items()

        map = map_processor.get_map()

        # Counters for entrance and exit nodes
        entrance_count = 0
        exit_count = 0

        # Iterate through each node and check the label
        for node in map["nodes"]:
            if node["label"] == "Entrance":
                entrance_count += 1
            elif node["label"] == "Exit":
                exit_count += 1

        self.assertEqual(entrance_count, 1)
        self.assertEqual(exit_count, 1)

    def test_adding_items(self):
        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=3, percent_connected=0.25
        ).get_json()

        map_processor = MapProcessor(unprocessed_map)
        map_processor = map_processor.add_entrance_exit()

        map_processor.set_item_range(1, 1)
        map_processor = map_processor.add_items()

        map = map_processor.get_map()

        item_count = 0

        # Iterate through each node and check the label
        for node in map["nodes"]:
            if len(node["game_info"]["items"]) > 0:
                item_count += 1

        self.assertEqual(len(map["nodes"]), item_count)

    def test_adding_encounters(self):
        map_generator = MapGenerator()
        unprocessed_map = map_generator.generate(
            num_rooms=3, percent_connected=0.25
        ).get_json()

        map_processor = MapProcessor(unprocessed_map)
        map_processor = map_processor.add_entrance_exit()

        map_processor.set_encounter_probability(1)
        map_processor = map_processor.add_encounters()

        map = map_processor.get_map()

        item_count = 0

        # Iterate through each node and check the label
        for node in map["nodes"]:
            if len(node["game_info"]["encounters"]) > 0:
                item_count += 1

        self.assertEqual(len(map["nodes"]), item_count)
