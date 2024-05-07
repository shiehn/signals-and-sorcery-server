import random
import uuid


class EncounterGenerator:
    def generate_encounters(self, num_of_items):
        encounters = []

        for i in range(num_of_items):
            encounter_type = random.choice(["monster"])
            item = {
                "encounter_id": str(uuid.uuid4()),
                "encounter_type": encounter_type,
                "encounter_size": "6x6",
                "aesthetic": {
                    "description": "",
                    "image": "",
                },
            }

            encounters.append(item)

        return encounters
