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
                "game_info": {
                    "items": [],
                    "encounters": [],
                    "doors": [],
                    "environment": {
                        "aesthetic": {
                            "description": "",
                            "image": "",
                        },
                    },
                },
            }
            for n in self.dist_graph.nodes()
        ]

    def get_full_graph(self):
        return self.dist_graph

    def get_json(self):
        graph_json = dict(nodes=self.get_node_json(), edges=self.get_edge_json())

        return graph_json

    def generate(self, num_rooms: int, percent_connected: float = 0.25):
        self.num_rooms = num_rooms
        self.percent_connected = percent_connected

        self.dist_graph = self.gen_connected_graph()

        return self

    def gen_connected_graph(self):
        # Generate UUIDs for each node
        uuids = [str(uuid.uuid4()) for _ in range(self.num_rooms)]

        # Start by creating a minimum spanning tree to ensure all nodes are connected
        graph = nx.Graph()
        graph.add_nodes_from(uuids)

        # Creating a path connecting all nodes, ensuring graph is connected
        for i in range(self.num_rooms - 1):
            graph.add_edge(uuids[i], uuids[i + 1])

        # Add more edges based on the desired percent of connectivity
        potential_edges = [
            (uuids[i], uuids[j])
            for i in range(self.num_rooms)
            for j in range(i + 1, self.num_rooms)
        ]
        random.shuffle(
            potential_edges
        )  # Shuffle potential edges to randomize edge addition

        # Calculate the number of edges to add to reach the desired connectivity
        num_all_possible_edges = len(potential_edges)
        num_edges_to_add = int(self.percent_connected * num_all_possible_edges) - (
            self.num_rooms - 1
        )

        added_edges = 0
        for edge in potential_edges:
            if added_edges >= num_edges_to_add:
                break
            if not graph.has_edge(*edge):
                graph.add_edge(*edge)
                added_edges += 1

        print(
            f"Added {self.num_rooms - 1 + added_edges} edges total; {added_edges} additional edges beyond the initial spanning tree"
        )

        return graph
