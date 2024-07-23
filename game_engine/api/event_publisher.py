from game_models.models import GameEvent
import logging
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)


class EventPublisher:
    def publish_sync(self, user_id: str, event: str, payload: dict = None) -> bool:
        try:
            if payload is None:
                payload = {}  # Ensure payload defaults to an empty dictionary

            GameEvent.objects.create(user_id=user_id, event=event, payload=payload)
            return True
        except Exception as e:
            logger.error(f"Error publishing event: {e}")
            return False

    async def publish_async(
        self, user_id: str, event: str, payload: dict = None
    ) -> bool:
        try:
            if payload is None:
                payload = {}  # Ensure payload defaults to an empty dictionary

            await sync_to_async(GameEvent.objects.create)(
                user_id=user_id, event=event, payload=payload
            )
            return True
        except Exception as e:
            logger.error(f"Error publishing event: {e}")
            return False
