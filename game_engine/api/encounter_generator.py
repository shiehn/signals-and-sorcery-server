import random
import uuid
from game_engine.conf.config import IMG_ENCOUNTER_PLACEHOLDER


class EncounterGenerator:
    def generate_encounters(self, num_of_items):
        encounters = []

        for i in range(num_of_items):
            encounter_type = random.choice(["monster"])
            item = {
                "encounter_id": str(uuid.uuid4()),
                "encounter_type": encounter_type,
                "encounter_level": random.randint(1, 10),
                "aesthetic": {
                    "description": "",
                    "image": IMG_ENCOUNTER_PLACEHOLDER,
                },
            }

            encounters.append(item)

        return encounters
