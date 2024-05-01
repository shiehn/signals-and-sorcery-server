import random
import uuid


class ItemGenerator:
    def generate_item(self, num_of_items):
        items = []

        for i in range(num_of_items):
            item_type = random.choice(["weapon", "armor", "potion"])
            item = {
                "item_id": str(uuid.uuid4()),
                "item_type": item_type,
                "item_size": "4x6",
            }

            items.append(item)

        return items
