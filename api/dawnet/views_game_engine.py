from game_engine.messages import handle_user_message
from rest_framework import status, views
from rest_framework.response import Response


def handle_message(message: str, token: str):
    # This function should be called by the game engine to handle the user message
    # The game engine should pass the message
    return handle_user_message(message, token)


class GameQueryView(views.APIView):
    authentication_classes = []  # Disables authentication
    permission_classes = []  # Disables permission

    def post(self, request, *args, **kwargs):
        # Extract data from the request body
        token = request.data.get("token")
        query = request.data.get("query")

        if not token or not query:
            # If either token or query is missing, return a bad request response
            return Response(
                {"error": "Both 'token' and 'query' are required in the request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Handle the user's message
        response_message = handle_message(query, token)

        # Return a success response with the handled message or other response data
        return Response(
            {"status": "success", "response": response_message},
            status=status.HTTP_200_OK,
        )
