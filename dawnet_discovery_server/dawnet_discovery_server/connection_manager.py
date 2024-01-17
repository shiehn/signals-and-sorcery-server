import asyncio
import json
import logging

import websockets

from dawnet_discovery_server.byoc_api import update_connection_status


class ConnectionManager:
    def __init__(self):
        self.connections = {}  # Local in-memory store for token to connection mapping
        #self.connections_lock = asyncio.Lock()  # Lock to protect the connections dictionary

    async def add_connection(self, token, websocket):
        logging.info("ATTEMPTING TO REGISTER TOKEN:WEBSOCKET = " + str(token) + " : " + str(websocket))
        #async with self.connections_lock:
        logging.info("REGISTERED TOKEN:WEBSOCKET = " + str(token) + " : " + str(websocket))
        self.connections[token] = websocket
        await update_connection_status(token, 1)

    async def remove_connection(self, token):
        #async with self.connections_lock:
        if token in self.connections:
            del self.connections[token]
            await update_connection_status(token, 0)

    async def check_client_health(self):
        #async with self.connections_lock:
        disconnected_tokens = []
        for token, websocket in self.connections.items():
            try:
                await websocket.ping()
            except websockets.exceptions.ConnectionClosed:
                disconnected_tokens.append(token)

        for token in disconnected_tokens:
            print("REMOVING DEAD CONNECTION: " + str(token))
            await self.remove_connection(token)

    async def get_websocket(self, token):
        #async with self.connections_lock:
        return self.connections.get(token)

    async def send_message_to_token(self, token: str, message_id: str, message: str):
        websocket = await self.get_websocket(token)
        if not websocket:
            print(f"No active connection for token: {token}")
            return False
        try:
            # inject message_id into message
            message['message_id'] = message_id

            json_message = json.dumps(message)

            print("--------------------------------------------------")
            print("TOO: " + str(token))
            print("SEND: " + str(json_message))
            print("--------------------------------------------------")

            await websocket.send(json_message)

            return True
        except websockets.exceptions.ConnectionClosed:
            print(f"Connection for token {token} closed before message could be sent.")
            await self.remove_connection(token)
            return False
