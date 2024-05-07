import unittest
from game_engine.api.map_generator import MapGenerator
from game_engine.api.map_processor import MapProcessor
import networkx as nx

# python manage.py test game_engine.tests.test_generator


class TestMapGenerator(unittest.TestCase):
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

    def test_all_nodes_are_traversable(self):
        # Test the graph for 30% connectivity
        num_rooms = 10
        percent_connected = 0.3
        map_generator = MapGenerator()
        graph = map_generator.generate(num_rooms, percent_connected).get_full_graph()

        # Check if the graph is connected
        self.assertTrue(nx.is_connected(graph), "Graph should be connected")

        # Calculate the expected number of edges
        num_all_possible_edges = num_rooms * (num_rooms - 1) // 2
        expected_edges = int(percent_connected * num_all_possible_edges)

        # Check if the actual number of edges is close to the expected number
        # Allow some margin as randomness can slightly vary the edge count
        actual_edges = graph.number_of_edges()
        self.assertTrue(
            abs(actual_edges - expected_edges)
            <= 3,  # Adjust tolerance based on your needs
            f"Expected around {expected_edges} edges, but got {actual_edges}",
        )
