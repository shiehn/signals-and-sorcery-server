def generate_image(description):
    return "https://alphauniverseglobal.media.zestyio.com/Alpha-Universe-BTS-Christopher-Byler-1.jpeg?width=400&height=400"


def generate_description(type, aesthetic):
    return f"This is a placeholder description for {type} in {aesthetic} style."


class AestheticGenerator:
    def __init__(self, aesthetic="default", map=None):
        self.aesthetic = aesthetic
        self.map = map

    def ensure_list(self, dictionary, key):
        if key not in dictionary:
            dictionary[key] = []

    def add_item_aesthetic(self):
        for node in self.map["nodes"]:
            self.ensure_list(node["game_info"], "items")
            for item in node["game_info"]["items"]:
                item["aesthetic"] = {
                    "description": generate_description("item", self.aesthetic),
                    "image": generate_image("item"),
                }

    def add_encounter_aesthetic(self):
        for node in self.map["nodes"]:
            self.ensure_list(node["game_info"], "encounters")
            for encounter in node["game_info"]["encounters"]:
                encounter["aesthetic"] = {
                    "description": generate_description("encounter", self.aesthetic),
                    "image": generate_image("encounter"),
                }

    def add_environment_aesthetic(self):
        for node in self.map["nodes"]:
            if "environment" not in node["game_info"]:
                node["game_info"]["environment"] = {}
            node["game_info"]["environment"]["aesthetic"] = {
                "description": generate_description("environment", self.aesthetic),
                "image": generate_image("environment"),
            }

    def add_all_aesthetics(self):
        self.add_item_aesthetic()
        self.add_encounter_aesthetic()
        self.add_environment_aesthetic()


# Example usage:
map_data = {
    "nodes": [
        # Nodes data as specified earlier
    ]
}

gen = AestheticGenerator(aesthetic="fantasy", map=map_data)
gen.add_all_aesthetics()
print(map_data)
