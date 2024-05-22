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

    def add_item_aesthetic(self):
        for node in self.map["nodes"]:
            self.ensure_list(node["game_info"], "items")
            for item in node["game_info"]["items"]:
                item["aesthetic"] = {
                    "description": self.asset_generator.generate_description(
                        "weapon", self.aesthetic
                    ),
                    "image": self.asset_generator.generate_image(
                        "weapon", self.aesthetic
                    ),
                }

    def add_encounter_aesthetic(self):
        for node in self.map["nodes"]:
            self.ensure_list(node["game_info"], "encounters")
            for encounter in node["game_info"]["encounters"]:
                encounter["aesthetic"] = {
                    "description": self.asset_generator.generate_description(
                        "monster", self.aesthetic
                    ),
                    "image": self.asset_generator.generate_image(
                        "monster", self.aesthetic
                    ),
                }

    def add_environment_aesthetic(self):
        for node in self.map["nodes"]:
            items_info = [
                item["aesthetic"]["description"]
                for item in node["game_info"].get("items", [])
            ]
            encounters_info = [
                encounter["aesthetic"]["description"]
                for encounter in node["game_info"].get("encounters", [])
            ]

            combined_description = (
                f"environment with {' and '.join(items_info + encounters_info)}"
            )

            if "environment" not in node["game_info"]:
                node["game_info"]["environment"] = {}

            node["game_info"]["environment"]["aesthetic"] = {
                "description": self.asset_generator.generate_description(
                    combined_description, self.aesthetic
                ),
                "image": self.asset_generator.generate_image(
                    combined_description, self.aesthetic
                ),
            }

    def add_all_aesthetics(self):
        self.add_item_aesthetic()
        self.add_encounter_aesthetic()
        self.add_environment_aesthetic()

        return self.map


# Example usage:
map_data = {
    "nodes": [
        # Nodes data as specified earlier
    ]
}
