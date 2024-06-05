from byo_network_hub.models import GameEvent

import logging

logger = logging.getLogger(__name__)


class EventPublisher:
    def publish(self, user_id: str, event: str):
        try:
            event = GameEvent.objects.create(user_id=user_id, event=event)
            return True
        except Exception as e:
            logger.error(f"Error publishing event: {e}")
            return False
