import unittest
from game_engine.api.aesthetic_generator import AestheticGenerator


class TestAestheticGenerator(unittest.TestCase):
    def test_add_item_aesthetic_with_existing_items(self):
        map_data = {"nodes": [{"game_info": {"items": [{}]}}]}
        expected_description = (
            "This is a placeholder description for item in fantasy style."
        )
        expected_image = "https://alphauniverseglobal.media.zestyio.com/Alpha-Universe-BTS-Christopher-Byler-1.jpeg?width=400&height=400"

        gen = AestheticGenerator(aesthetic="fantasy", map=map_data)
        gen.add_item_aesthetic()

        self.assertIn("aesthetic", map_data["nodes"][0]["game_info"]["items"][0])
        self.assertEqual(
            map_data["nodes"][0]["game_info"]["items"][0]["aesthetic"]["description"],
            expected_description,
        )
        self.assertEqual(
            map_data["nodes"][0]["game_info"]["items"][0]["aesthetic"]["image"],
            expected_image,
        )

    def test_add_item_aesthetic_with_no_items(self):
        map_data = {"nodes": [{"game_info": {}}]}
        gen = AestheticGenerator(aesthetic="fantasy", map=map_data)
        gen.add_item_aesthetic()

        self.assertEqual(len(map_data["nodes"][0]["game_info"]["items"]), 0)

    def test_add_encounter_aesthetic_with_missing_encounters(self):
        map_data = {"nodes": [{"game_info": {}}]}
        gen = AestheticGenerator(aesthetic="fantasy", map=map_data)
        gen.add_encounter_aesthetic()

        self.assertEqual(len(map_data["nodes"][0]["game_info"]["encounters"]), 0)

    def test_add_all_aesthetics_complete(self):
        map_data = {"nodes": [{"game_info": {"items": [{}], "encounters": [{}]}}]}
        expected_description = (
            "This is a placeholder description for environment in fantasy style."
        )
        expected_image = "https://alphauniverseglobal.media.zestyio.com/Alpha-Universe-BTS-Christopher-Byler-1.jpeg?width=400&height=400"

        gen = AestheticGenerator(aesthetic="fantasy", map=map_data)
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
            expected_image,
        )


if __name__ == "__main__":
    unittest.main()
