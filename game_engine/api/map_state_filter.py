class MapStateFilter:
    def __init__(self, map_graph):
        self.map_graph = map_graph

    def filter(self, map_state):
        # Create a set of consumed IDs for quick lookup
        consumed_ids = {str(state.item_id) for state in map_state if state.consumed}
        filtered_map = {
            "nodes": [],
            "edges": self.map_graph.get("edges", []),  # Ensure edges are included
        }

        # Iterate over the nodes and filter out consumed items and encounters
        for node in self.map_graph["nodes"]:
            filtered_node = node.copy()
            filtered_node["game_info"] = filtered_node.get("game_info", {}).copy()

            # Filter items
            filtered_items = [
                item
                for item in filtered_node["game_info"].get("items", [])
                if item["item_id"] not in consumed_ids
            ]
            filtered_node["game_info"]["items"] = filtered_items

            # Filter encounters
            filtered_encounters = [
                encounter
                for encounter in filtered_node["game_info"].get("encounters", [])
                if encounter["encounter_id"] not in consumed_ids
            ]
            filtered_node["game_info"]["encounters"] = filtered_encounters

            filtered_map["nodes"].append(filtered_node)

        return filtered_map
