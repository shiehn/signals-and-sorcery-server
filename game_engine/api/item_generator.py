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
                "item_level": random.randint(1, 100),
                "aesthetic": {
                    "description": "",
                    "image": IMG_ITEM_PLACEHOLDER,
                },
            }

            items.append(item)

        return items

    def generate_unarmed_item(self):
        return {
            "item_id": str(uuid.uuid4()),
            "item_type": "unarmed",
            "item_level": 0,
            "aesthetic": {
                "description": "unarmed",
                "image": IMG_ITEM_PLACEHOLDER,
            },
        }
