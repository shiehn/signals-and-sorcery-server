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
            {"id": n, "label": n[:3], "shape": "box"} for n in self.dist_graph.nodes()
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

        # Print nodes and edges
        # print("Nodes of the graph:")
        # for node in graph.nodes():
        #     print(node)
        # print("\nEdges of the graph:")
        # for edge in graph.edges():
        #     print(edge)

        return graph

    # rooms = []
    #
    # print(f"Generating {self.num_rooms} rooms...")
    #
    # for i in range(self.num_rooms):
    #     room = MapRoom(room_id=str(uuid.uuid4()))
    #     rooms.append(room)
    #
    # print(f"Rooms generated: {rooms}")
    #
    # print("Generating Doors & Connections...")
    #
    # # min of 2 rooms (entrance and exit)
    # # every other room can have 0-3 doors
    # if self.num_rooms < 2:
    #     print("Error: Must have at least 2 rooms")
    #     return
    #
    # elif self.num_rooms == 2:
    #     rooms[0].set_label("Entrance")
    #     rooms[1].set_label("Exit")
    #
    #     rooms[0].add_connection(rooms[1].id)
    #     rooms[1].add_connection(rooms[0].id)
    #
    #     print(f"Entrance and exit generated: {rooms}")
    #     return
    #
    # else:
