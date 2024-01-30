import json
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import asyncio
import websockets


class HealthCheckView(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    async def check_websocket_connection(self):
        uri = f"ws://{os.environ.get('WEB_SOCKET_SERVER_IP')}:{os.environ.get('WEB_SOCKET_PORT')}"
        try:
            async with websockets.connect(uri, close_timeout=5) as ws:
                await ws.send(json.dumps({"type": "healthcheck"}))
                response = await ws.recv()
                return json.loads(response)
        except Exception as e:
            return {"status": "failure", "reason": str(e)}

    def get(self, request, *args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.check_websocket_connection())
        if result.get("status") == "success":
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_503_SERVICE_UNAVAILABLE)
