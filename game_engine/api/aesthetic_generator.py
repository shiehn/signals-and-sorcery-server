import asyncio
from game_engine.gen_ai.asset_generator import AssetGenerator
from game_engine.api.riddle_generator import RiddleGenerator


class AestheticGenerator:
    def __init__(
        self, aesthetic="default", map=None, asset_generator: AssetGenerator = None
    ):
        self.aesthetic = aesthetic
        self.map = map
        self.asset_generator = asset_generator

    def ensure_list(self, dictionary, key):
        if key not in dictionary:
            dictionary[key] = []

    async def add_item_aesthetic(self):
        for node in self.map["nodes"]:
            self.ensure_list(node["game_info"], "items")
            for item in node["game_info"]["items"]:
                item_type = item.get("item_type", "item")
                item["aesthetic"] = {
                    "description": await self.asset_generator.generate_description(
                        item_type, self.aesthetic
                    ),
                    "image": await self.asset_generator.generate_image(
                        item_type, self.aesthetic
                    ),
                }

    async def add_encounter_aesthetic(self):
        for node in self.map["nodes"]:
            self.ensure_list(node["game_info"], "encounters")
            for encounter in node["game_info"]["encounters"]:
                encounter_type = encounter.get("encounter_type", "encounter")
                encounter["aesthetic"] = {
                    "description": await self.asset_generator.generate_description(
                        encounter_type, self.aesthetic
                    ),
                    "image": await self.asset_generator.generate_image(
                        encounter_type, self.aesthetic
                    ),
                }

    async def add_environment_aesthetic(self):
        for node in self.map["nodes"]:
            items_info = [
                item["item_type"] for item in node["game_info"].get("items", [])
            ]
            encounters_info = [
                encounter["encounter_type"]
                for encounter in node["game_info"].get("encounters", [])
            ]

            combined_description = (
                f"environment with {' and '.join(items_info + encounters_info)}"
            )

            if "environment" not in node["game_info"]:
                node["game_info"]["environment"] = {}

            node["game_info"]["environment"]["aesthetic"] = {
                "description": await self.asset_generator.generate_description(
                    combined_description, self.aesthetic
                ),
                "image": await self.asset_generator.generate_image(
                    combined_description, self.aesthetic
                ),
            }

    async def add_clues(self):
        riddle_generator = RiddleGenerator(self.asset_generator)

        # Generate the correct password
        correct_password = riddle_generator.generate_password()

        for node in self.map["nodes"]:
            # Get setting and lore from node's environment aesthetic description
            setting_and_lore = node["game_info"]["environment"]["aesthetic"][
                "description"
            ]

            # Generate clues based on the correct password and setting
            clues = await riddle_generator.generate_clues(
                correct_password, setting_and_lore
            )

            # Generate incorrect passwords
            incorrect_passwords = riddle_generator.generate_incorrect_passwords(
                correct_password
            )

            # Store the password and clues in the node's game_info
            node["game_info"]["riddle"] = {
                "password": {
                    "correct": correct_password,
                    "incorrect": incorrect_passwords,
                },
                "clues": clues,
            }

    async def add_all_aesthetics(self):
        # Run these three tasks concurrently
        await asyncio.gather(
            self.add_item_aesthetic(),
            self.add_encounter_aesthetic(),
            self.add_environment_aesthetic(),
        )
        # After the above tasks have completed, run this
        await self.add_clues()

        return self.map
