import random
import uuid
import networkx as nx


class MapGenerator:
    def __init__(self):
        self.num_rooms = 0
        self.dist_graph = None

    def get_edge_json(self):
        return [{"from": u, "to": v} for u, v in self.dist_graph.edges()]

    def get_node_json(self):
        return [
            {
                "id": n,
                "label": n[:3],
                "shape": "box",
                "game_info": {"items": [], "encounters": [], "doors": []},
            }
            for n in self.dist_graph.nodes()
        ]

    def get_json(self):
        graph_json = dict(nodes=self.get_node_json(), edges=self.get_edge_json())

        return graph_json

    def generate(self, num_rooms: int, percent_connected: float = 0.25):
        self.num_rooms = num_rooms
        self.percent_connected = percent_connected

        self.dist_graph = self.gen_distributed_graph(percent_connected)

        return self

    def gen_distributed_graph(self, percent_connected):
        # Generate UUIDs for each node
        uuids = [str(uuid.uuid4()) for _ in range(self.num_rooms)]
        # Generate the Erdős–Rényi graph G(n, p)
        graph = nx.Graph()
        # Add nodes with UUIDs
        graph.add_nodes_from(uuids)
        p = percent_connected  # probability of edge creation
        added = 0
        not_added = 0
        for i in range(self.num_rooms):
            for j in range(
                i + 1, self.num_rooms
            ):  # to ensure each pair is considered only once
                if random.random() < p:
                    graph.add_edge(uuids[i], uuids[j])
                    added += 1
                else:
                    not_added += 1

        print(f"Added {added} edges, did not add {not_added} edges")

        return graph
