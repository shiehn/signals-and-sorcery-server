import random
from game_engine.api.item_generator import ItemGenerator


class MapProcessor:
    def __init__(self, map_graph):
        self.map_graph = map_graph
        self.item_range_min = 0
        self.item_range_max = 2

    def set_item_range(self, item_range_min, item_range_max):
        self.item_range_min = item_range_min
        self.item_range_max = item_range_max

        return self

    def add_entrance_exit(self):
        random_nodes = random.sample(self.map_graph["nodes"], 2)

        # Ensure the color attribute exists for each node, if not, initialize it
        if "color" not in random_nodes[0]:
            random_nodes[0]["color"] = {}
        if "color" not in random_nodes[1]:
            random_nodes[1]["color"] = {}

        # Entrance
        random_nodes[0]["label"] = "Entrance"
        random_nodes[0]["color"]["background"] = "green"

        # Exit
        random_nodes[1]["label"] = "Exit"
        random_nodes[1]["color"]["background"] = "red"

        return self

    def add_items(self):
        item_generator = ItemGenerator()

        for node in self.map_graph["nodes"]:
            random_number = random.randint(self.item_range_min, self.item_range_max)
            node["game_info"]["items"] = item_generator.generate_item(random_number)

        return self

    def get_map(self):
        return self.map_graph
