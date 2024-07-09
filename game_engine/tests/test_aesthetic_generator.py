import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from game_engine.api.aesthetic_generator import AestheticGenerator
from game_engine.gen_ai.asset_generator import AssetGenerator
from game_engine.api.riddle_generator import RiddleGenerator


class TestAestheticGenerator(unittest.TestCase):
    def setUp(self):
        # Setup the mock for AssetGenerator
        self.mock_asset_generator = MagicMock(spec=AssetGenerator)
        self.mock_asset_generator.generate_image.return_value = "https://alphauniverseglobal.media.zestyio.com/Alpha-Universe-BTS-Christopher-Byler-1.jpeg?width=400&height=400"
        self.mock_asset_generator.generate_description.return_value = (
            "This is a placeholder description."
        )
        self.mock_asset_generator.generate_riddle = AsyncMock(
            return_value="This is a riddle clue."
        )

    def test_add_item_aesthetic_with_existing_items(self):
        map_data = {"nodes": [{"game_info": {"items": [{"item_type": "item"}]}}]}
        expected_description = "This is a placeholder description."

        gen = AestheticGenerator(
            aesthetic="fantasy", map=map_data, asset_generator=self.mock_asset_generator
        )
        asyncio.run(gen.add_item_aesthetic())

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
        asyncio.run(gen.add_item_aesthetic())

        self.assertEqual(len(map_data["nodes"][0]["game_info"]["items"]), 0)

    def test_add_encounter_aesthetic_with_missing_encounters(self):
        map_data = {"nodes": [{"game_info": {}}]}
        gen = AestheticGenerator(
            aesthetic="fantasy", map=map_data, asset_generator=self.mock_asset_generator
        )
        asyncio.run(gen.add_encounter_aesthetic())

        self.assertEqual(len(map_data["nodes"][0]["game_info"]["encounters"]), 0)

    def test_add_all_aesthetics_complete(self):
        map_data = {
            "nodes": [
                {
                    "game_info": {
                        "items": [{"item_type": "item"}],
                        "encounters": [{"encounter_type": "encounter"}],
                    }
                }
            ]
        }
        expected_description = "This is a placeholder description."

        gen = AestheticGenerator(
            aesthetic="fantasy", map=map_data, asset_generator=self.mock_asset_generator
        )
        asyncio.run(gen.add_all_aesthetics())

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

    def test_add_clues(self):
        map_data = {
            "nodes": [
                {
                    "game_info": {
                        "environment": {
                            "aesthetic": {"description": "A beautiful forest"}
                        }
                    }
                }
            ]
        }
        gen = AestheticGenerator(
            aesthetic="fantasy", map=map_data, asset_generator=self.mock_asset_generator
        )

        # Mock the password generation and clue generation methods
        gen.asset_generator.generate_riddle = AsyncMock(
            return_value="This is a riddle clue."
        )
        RiddleGenerator.generate_password = MagicMock(return_value="correct_password")
        RiddleGenerator.generate_incorrect_passwords = MagicMock(
            return_value=["wrong_ans_a", "wrong_ans_b", "wrong_ans_c"]
        )

        asyncio.run(gen.add_clues())

        riddle_info = map_data["nodes"][0]["game_info"]["riddle"]
        self.assertEqual(riddle_info["password"]["correct"], "correct_password")
        self.assertEqual(
            riddle_info["password"]["incorrect"],
            ["wrong_ans_a", "wrong_ans_b", "wrong_ans_c"],
        )
        self.assertEqual(riddle_info["clues"], ["This is a riddle clue."])


if __name__ == "__main__":
    unittest.main()
