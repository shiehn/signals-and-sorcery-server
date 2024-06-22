import asyncio
from game_engine.gen_ai.asset_generator import AssetGenerator


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

    async def add_all_aesthetics(self):
        await asyncio.gather(
            self.add_item_aesthetic(),
            self.add_encounter_aesthetic(),
            self.add_environment_aesthetic(),
        )

        return self.map
