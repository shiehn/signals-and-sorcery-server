import unittest
from unittest.mock import MagicMock
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            "byo_network_hub",
            "game_engine",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
    )
    django.setup()

from game_engine.api.combat_processor import CombatProcessor


class TestCombatProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = CombatProcessor()

    def test_create_combat_stats_encounter_victory(self):
        encounter = {
            "encounter_id": "encounter_1",
            "encounter_level": 5,
            "aesthetic": {
                "description": "",
                "image": "IMG_ENCOUNTER_PLACEHOLDER",
            },
        }
        item = MagicMock()
        item.item_id = "item_1"
        item.item_details = {
            "item_level": 60,
            "aesthetic": {
                "description": "",
                "image": "IMG_ITEM_PLACEHOLDER",
            },
        }
        roll = 30
        expected_stats = {
            "phase": "encounter-victory",
            "encounter": 5,
            "modifiers": [
                {
                    "item": "item_1",
                    "modifier": 60,
                },
            ],
            "chance_of_success_base": 50,
            "chance_of_success_total": 110,
            "result": 30,
        }

        stats = self.processor.create_combat_stats(encounter, item, roll)
        self.assertEqual(stats, expected_stats)

    def test_create_combat_stats_encounter_loss(self):
        encounter = {
            "encounter_id": "encounter_2",
            "encounter_level": 8,
            "aesthetic": {
                "description": "",
                "image": "IMG_ENCOUNTER_PLACEHOLDER",
            },
        }
        item = MagicMock()
        item.item_id = "item_2"
        item.item_details = {
            "item_level": 30,
            "aesthetic": {
                "description": "",
                "image": "IMG_ITEM_PLACEHOLDER",
            },
        }
        roll = 90
        expected_stats = {
            "phase": "encounter-loss",
            "encounter": 8,
            "modifiers": [
                {
                    "item": "item_2",
                    "modifier": 30,
                },
            ],
            "chance_of_success_base": 20,
            "chance_of_success_total": 50,
            "result": 90,
        }

        stats = self.processor.create_combat_stats(encounter, item, roll)
        self.assertEqual(stats, expected_stats)

    def test_create_combat_stats_with_minimal_success(self):
        encounter = {
            "encounter_id": "encounter_3",
            "encounter_level": 1,
            "aesthetic": {
                "description": "",
                "image": "IMG_ENCOUNTER_PLACEHOLDER",
            },
        }
        item = MagicMock()
        item.item_id = "item_3"
        item.item_details = {
            "item_level": 5,
            "aesthetic": {
                "description": "",
                "image": "IMG_ITEM_PLACEHOLDER",
            },
        }
        roll = 95
        expected_stats = {
            "phase": "encounter-victory",
            "encounter": 1,
            "modifiers": [
                {
                    "item": "item_3",
                    "modifier": 5,
                },
            ],
            "chance_of_success_base": 90,
            "chance_of_success_total": 95,
            "result": 95,
        }

        stats = self.processor.create_combat_stats(encounter, item, roll)
        self.assertEqual(stats, expected_stats)

    def test_create_combat_stats_none_values(self):
        roll = 50
        expected_stats = {
            "phase": "no-encounter-or-item",
            "encounter": None,
            "modifiers": [],
            "chance_of_success_base": None,
            "chance_of_success_total": None,
            "result": roll,
        }

        stats = self.processor.create_combat_stats(None, None, roll)
        self.assertEqual(stats, expected_stats)


if __name__ == "__main__":
    unittest.main()
