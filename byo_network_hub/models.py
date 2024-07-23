from django.db import models
import uuid


# GAME ENGINE MODELS -----------------------------------------------
class GameElementLookup(models.Model):
    element_id = models.UUIDField(primary_key=True, unique=True)
    user_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)


class GameState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(
        unique=True, null=False, blank=False
    )  # Enforce uniqueness
    level = models.IntegerField()
    aesthetic = models.CharField(max_length=1024)
    art_style = models.CharField(max_length=1024)
    setting = models.CharField(max_length=4096)
    map_id = models.UUIDField(default=uuid.UUID(int=0), null=True, blank=True)
    environment_id = models.UUIDField(null=True, blank=True)  # Allow null values
    environment_img = models.CharField(
        max_length=1024, null=True, blank=True
    )  # Allow null values
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class GameMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.IntegerField()
    description = models.TextField()
    map_graph = models.JSONField()  # Add this line for the JSON field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class GameMapState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    map_id = models.UUIDField()
    item_id = models.UUIDField()
    aesthetic = models.CharField(max_length=1024)
    consumed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class GameInventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    map_id = models.UUIDField()
    user_id = models.UUIDField()
    item_id = models.UUIDField()
    item_details = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class GameUpdateQueue(models.Model):
    user_id = models.UUIDField(unique=True)  # Ensures each user_id is unique
    level = models.IntegerField(default=0)

    # Define choices for status
    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("started", "Started"),
        ("completed", "Completed"),
        ("error", "Error"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="queued")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id} - {self.status}"


class GameEvent(models.Model):
    user_id = models.UUIDField()
    EVENT_CHOICES = [
        ("level-up-ready", "LevelUpReady"),
        ("level-up-complete", "LevelUpComplete"),
        ("encounter-start", "EncounterStart"),
        ("encounter-victory", "EncounterVictory"),
        ("encounter-loss", "EncounterLoss"),
        ("inventory-update", "InventoryUpdate"),
    ]
    event = models.CharField(max_length=32, choices=EVENT_CHOICES, default="combat")
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.event}"
