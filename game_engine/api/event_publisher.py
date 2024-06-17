from byo_network_hub.models import GameEvent

import logging

logger = logging.getLogger(__name__)


class EventPublisher:
    def publish(self, user_id: str, event: str, payload: dict = None) -> bool:
        try:
            if payload is None:
                payload = {}  # Ensure payload defaults to an empty dictionary

            event = GameEvent.objects.create(
                user_id=user_id, event=event, payload=payload
            )
            return True
        except Exception as e:
            logger.error(f"Error publishing event: {e}")
            return False
