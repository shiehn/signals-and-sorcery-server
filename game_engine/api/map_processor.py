import random
from game_engine.api.item_generator import ItemGenerator
from game_engine.api.encounter_generator import EncounterGenerator
import networkx as nx


class MapProcessor:
    def __init__(self, map_graph):
        self.map_graph = map_graph
        self.item_range_min = 0
        self.item_range_max = 2
        self.encounter_probability = 0.25
        self.nx_graph = self.build_networkx_graph()

    def set_item_range(self, item_range_min, item_range_max):
        self.item_range_min = item_range_min
        self.item_range_max = item_range_max

        return self

    def set_encounter_probability(self, encounter_probability):
        self.encounter_probability = encounter_probability

        return self

    def build_networkx_graph(self):
        nx_graph = nx.Graph()
        for edge in self.map_graph["edges"]:
            nx_graph.add_edge(edge["from"], edge["to"])
        return nx_graph

    def find_furthest_nodes(self):
        # Choose an arbitrary starting node (first node in the list)
        start_node = self.map_graph["nodes"][0]["id"]
        # Perform BFS to find the node furthest from start_node
        lengths = nx.single_source_shortest_path_length(self.nx_graph, start_node)
        furthest_node = max(lengths, key=lengths.get)

        # Perform BFS again from the furthest node found
        lengths = nx.single_source_shortest_path_length(self.nx_graph, furthest_node)
        furthest_from_furthest = max(lengths, key=lengths.get)

        return furthest_node, furthest_from_furthest

    def add_entrance_exit(self):
        entrance_id, exit_id = self.find_furthest_nodes()

        entrance_node = next(
            node for node in self.map_graph["nodes"] if node["id"] == entrance_id
        )
        exit_node = next(
            node for node in self.map_graph["nodes"] if node["id"] == exit_id
        )

        # Ensure the color attribute exists for each node, if not, initialize it
        entrance_node["label"] = "Entrance"
        entrance_node["color"]["border"] = "green"

        exit_node["label"] = "Exit"
        exit_node["color"]["border"] = "red"

        return self

    def add_items(self):
        item_generator = ItemGenerator()

        for node in self.map_graph["nodes"]:
            random_number = random.randint(self.item_range_min, self.item_range_max)
            node["game_info"]["items"] = item_generator.generate_item(random_number)

        return self

    def add_encounters(self):
        encounter_generator = EncounterGenerator()

        for node in self.map_graph["nodes"]:
            if (
                node.get("label") != "Entrance"
                and random.random() < self.encounter_probability
            ):
                node["game_info"][
                    "encounters"
                ] = encounter_generator.generate_encounters(1)

        return self

    def get_map(self):
        return self.map_graph
