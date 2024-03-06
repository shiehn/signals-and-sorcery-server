from django.db import models
import uuid


class Connection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    master_token = models.UUIDField()
    connection_token = models.UUIDField(unique=True)
    connection_name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class ConnectionStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plugin = models.BooleanField(null=False, default=False)
    compute = models.BooleanField(null=False, default=False)
    updated_at = models.DateTimeField(auto_now=True)

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


class RemoteImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    remote_name = models.CharField(max_length=100, null=False)
    remote_description = models.CharField(max_length=250, null=False)
    remote_category = models.CharField(max_length=100, null=False)
    remote_author = models.CharField(max_length=100, null=False)
    image_name = models.CharField(max_length=250, null=False)
    remote_version = models.CharField(max_length=25, null=False, default="v0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
