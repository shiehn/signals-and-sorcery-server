import random
import uuid
from game_engine.conf.config import IMG_ITEM_PLACEHOLDER


class ItemGenerator:
    def generate_item(self, num_of_items):
        items = []

        for i in range(num_of_items):
            item_type = random.choice(["weapon", "armor", "potion"])
            item = {
                "item_id": str(uuid.uuid4()),
                "item_type": item_type,
                "item_size": "4x6",
                "aesthetic": {
                    "description": "",
                    "image": IMG_ITEM_PLACEHOLDER,
                },
            }

            items.append(item)

        return items
