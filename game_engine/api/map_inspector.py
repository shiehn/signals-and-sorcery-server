class MapInspector:
    def __init__(self, map):
        self.map = map

    def extract_uuids(self):
        uuids = []

        # Extract node IDs
        for node in self.map.get("nodes", []):
            uuids.append(node["id"])

            # Extract item IDs within each node
            for item in node.get("game_info", {}).get("items", []):
                uuids.append(item["item_id"])

            # Extract encounter IDs within each node
            for encounter in node.get("game_info", {}).get("encounters", []):
                uuids.append(encounter["encounter_id"])

        return uuids

    def get_env_id_of_entrance(self):
        for node in self.map["nodes"]:
            if node["label"].lower() == "entrance":
                return node["id"]
        return None

    def get_env_id_of_exit(self):
        for node in self.map["nodes"]:
            if node["label"].lower() == "exit":
                return node["id"]
        return None

    def get_items_by_env_id(self, env_id):
        for node in self.map["nodes"]:
            if node["id"] == env_id:
                return node["game_info"]["items"]
        return None

    def get_encounters_by_env_id(self, env_id):
        for node in self.map["nodes"]:
            if node["id"] == env_id:
                return node["game_info"]["encounters"]
        return None

    def get_env_by_id(self, env_id):
        for node in self.map["nodes"]:
            if node["id"] == env_id:
                adjacent_env_ids = self.get_adjacent_environments(env_id)
                if adjacent_env_ids:
                    node["game_info"]["doors"] = adjacent_env_ids
                return node
        return None

    def get_adjacent_environments(self, env_id):
        adjacent_env_ids = []
        for edge in self.map["edges"]:
            if edge["to"] == env_id:
                adjacent_env_ids.append(edge["from"])
            elif edge["from"] == env_id:
                adjacent_env_ids.append(edge["to"])
        return adjacent_env_ids
