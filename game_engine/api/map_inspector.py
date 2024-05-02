class MapInspector:
    def __init__(self, map):
        self.map = map

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
