from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from game_engine.api.combat_processor import CombatProcessor
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from game_engine.rpg_chat_service import RPGChatService

import logging

logger = logging.getLogger(__name__)


class GameCombatAttackView(APIView):
    """
    Attack an encounter.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def set_action_outcome(self, user_id, action, outcome):
        rpg_chat_service = RPGChatService()
        rpg_chat_service.track_action_outcome(
            user_id=user_id, action=action, outcome=outcome
        )

    def post(self, request, format=None):
        if request.user is None:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_id = request.user.id

        item_id = request.data.get("item_id", None)

        logger.info("COMBAT user_id: " + str(user_id))
        logger.info("COMBAT item_id: " + str(item_id))

        if item_id is None:
            return Response(
                {"message": "Item is required in the payload"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        combat_processor = CombatProcessor()

        combat_result = combat_processor.attack(item_id)
        if combat_result == "encounter-victory" or combat_result == "encounter-loss":

            if combat_result == "encounter-victory":
                self.set_action_outcome(
                    user_id,
                    f"I attacked the encounter with item {str(item_id)}",
                    "and was victorious!",
                )
            else:
                self.set_action_outcome(
                    user_id,
                    f"I attacked the encounter with item {str(item_id)}",
                    "and was defeated.",
                )

            return Response({"message": combat_result}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": combat_result}, status=status.HTTP_400_BAD_REQUEST
            )
