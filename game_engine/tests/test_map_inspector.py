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
