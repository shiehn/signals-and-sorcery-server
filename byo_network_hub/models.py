from django.db import models
import uuid


class Connection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    master_token = models.UUIDField()
    connection_token = models.UUIDField(unique=True)
    connection_name = models.CharField(max_length=255)
    connection_type = models.CharField(max_length=255, default="unknown")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class ConnectionStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plugin = models.BooleanField(default=False)
    compute = models.BooleanField(default=False)
    loaded = models.BooleanField(default=False)
    plugin_updated_at = models.DateTimeField(
        auto_now_add=True
    )  # For the first creation
    compute_updated_at = models.DateTimeField(
        auto_now_add=True
    )  # For the first creation

    def __str__(self):
        return str(self.id)


class ComputeContract(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True
    )  # Set editable to True
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class BYOCMessageStates:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ABORTED = "aborted"
    ERROR = "error"


class BYOCMessageState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=255, null=False)
    request = models.JSONField()
    response = models.JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=50, null=True
    )  # 'progressing', 'completed', 'aborted','error'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


ELIXIR_CATEGORIES = [
    ("audio", "AUDIO"),
    ("video", "VIDEO"),
    ("image", "IMAGE"),
    ("text", "TEXT"),
]

PROCESSOR = [
    ("cpu", "CPU"),
    ("gpu", "GPU"),
]


class RemoteImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    remote_name = models.CharField(max_length=100, null=False)
    remote_description = models.CharField(max_length=250, null=False)
    remote_category = models.CharField(
        max_length=100, choices=ELIXIR_CATEGORIES, null=False
    )
    remote_author = models.CharField(max_length=100, null=False, blank=False)
    image_name = models.CharField(max_length=250, null=False)
    remote_version = models.CharField(max_length=25, null=False, default="v0")
    processor = models.CharField(
        max_length=25, choices=PROCESSOR, null=False, default="cpu"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class RemoteSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    remote_name = models.CharField(max_length=100, null=False)
    remote_description = models.CharField(max_length=250, null=False)
    remote_category = models.CharField(
        max_length=100, choices=ELIXIR_CATEGORIES, null=False
    )
    remote_author = models.CharField(max_length=100, null=False, blank=False)
    source_url = models.CharField(max_length=1500, null=False)
    colab_url = models.CharField(max_length=1500, null=True)
    remote_version = models.CharField(max_length=25, null=False, default="v0")
    processor = models.CharField(
        max_length=25, choices=PROCESSOR, null=False, default="cpu"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


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
    map_id = models.UUIDField()
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.event}"
