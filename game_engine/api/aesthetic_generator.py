def generate_description(type, aesthetic):
    return f"This is a placeholder description for {type} in {aesthetic} style."


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
                    "description": generate_description("item", self.aesthetic),
                    "image": self.asset_generator.generate_image(
                        "A potion in a " + self.aesthetic + " world."
                    ),
                }

    def add_encounter_aesthetic(self):
        for node in self.map["nodes"]:
            self.ensure_list(node["game_info"], "encounters")
            for encounter in node["game_info"]["encounters"]:
                encounter["aesthetic"] = {
                    "description": generate_description("encounter", self.aesthetic),
                    "image": self.asset_generator.generate_image(
                        "A monster in a " + self.aesthetic + " world."
                    ),
                }

    def add_environment_aesthetic(self):
        for node in self.map["nodes"]:
            if "environment" not in node["game_info"]:
                node["game_info"]["environment"] = {}
            node["game_info"]["environment"]["aesthetic"] = {
                "description": generate_description("environment", self.aesthetic),
                "image": self.asset_generator.generate_image(
                    "A room in a " + self.aesthetic + " world."
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
