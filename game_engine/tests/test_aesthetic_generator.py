import unittest
from unittest.mock import MagicMock
from game_engine.api.aesthetic_generator import AestheticGenerator
from game_engine.gen_ai.asset_generator import AssetGenerator


class TestAestheticGenerator(unittest.TestCase):
    def setUp(self):
        # Setup the mock for AssetGenerator
        self.mock_asset_generator = MagicMock(spec=AssetGenerator)
        self.mock_asset_generator.generate_image.return_value = "https://alphauniverseglobal.media.zestyio.com/Alpha-Universe-BTS-Christopher-Byler-1.jpeg?width=400&height=400"

    def test_add_item_aesthetic_with_existing_items(self):
        map_data = {"nodes": [{"game_info": {"items": [{}]}}]}
        expected_description = (
            "This is a placeholder description for item in fantasy style."
        )

        gen = AestheticGenerator(
            aesthetic="fantasy", map=map_data, asset_generator=self.mock_asset_generator
        )
        gen.add_item_aesthetic()

        self.assertIn("aesthetic", map_data["nodes"][0]["game_info"]["items"][0])
        self.assertEqual(
            map_data["nodes"][0]["game_info"]["items"][0]["aesthetic"]["description"],
            expected_description,
        )
        self.assertEqual(
            map_data["nodes"][0]["game_info"]["items"][0]["aesthetic"]["image"],
            self.mock_asset_generator.generate_image.return_value,
        )

    def test_add_item_aesthetic_with_no_items(self):
        map_data = {"nodes": [{"game_info": {}}]}
        gen = AestheticGenerator(
            aesthetic="fantasy", map=map_data, asset_generator=self.mock_asset_generator
        )
        gen.add_item_aesthetic()

        self.assertEqual(len(map_data["nodes"][0]["game_info"]["items"]), 0)

    def test_add_encounter_aesthetic_with_missing_encounters(self):
        map_data = {"nodes": [{"game_info": {}}]}
        gen = AestheticGenerator(
            aesthetic="fantasy", map=map_data, asset_generator=self.mock_asset_generator
        )
        gen.add_encounter_aesthetic()

        self.assertEqual(len(map_data["nodes"][0]["game_info"]["encounters"]), 0)

    def test_add_all_aesthetics_complete(self):
        map_data = {"nodes": [{"game_info": {"items": [{}], "encounters": [{}]}}]}
        expected_description = (
            "This is a placeholder description for environment in fantasy style."
        )

        gen = AestheticGenerator(
            aesthetic="fantasy", map=map_data, asset_generator=self.mock_asset_generator
        )
        gen.add_all_aesthetics()

        self.assertIn("aesthetic", map_data["nodes"][0]["game_info"]["environment"])
        self.assertEqual(
            map_data["nodes"][0]["game_info"]["environment"]["aesthetic"][
                "description"
            ],
            expected_description,
        )
        self.assertEqual(
            map_data["nodes"][0]["game_info"]["environment"]["aesthetic"]["image"],
            self.mock_asset_generator.generate_image.return_value,
        )


if __name__ == "__main__":
    unittest.main()
