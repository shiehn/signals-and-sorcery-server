import json
import logging

import websockets

from dawnet_discovery_server.byoc_api import (
    update_connection_status,
    add_connection_mapping,
)


class ConnectionManager:
    def __init__(self):
        self.registered_connections = {}  # Local in-memory store for token to connection mapping
        self.all_connections = set()  # Track all websocket connections
        # self.connections_lock = asyncio.Lock()  # Lock to protect the connections dictionary

    async def add_unregistered_connection(self, websocket):
        # async with self.connections_lock:
        self.all_connections.add(websocket)

    async def close_unregistered_connections(self):
        logging.info("UNREGISTERED CONNECTIONS: " + str(len(self.all_connections)))
        logging.info("REGISTERED CONNECTIONS: " + str(len(self.registered_connections)))

        # Collect websockets that need to be closed
        websockets_to_close = set()  # Use a set to avoid duplicates

        for websocket in self.all_connections:
            if await self.isWebSocketOrphaned(websocket):
                try:
                    await websocket.close()
                    logging.info(f"Closed unregistered websocket: {websocket}")
                    websockets_to_close.add(websocket)  # Add to the set of websockets to be removed
                except Exception as e:
                    logging.error(f"Error closing unregistered websocket: {e}")

        # Now, outside the loop, remove the collected websockets from self.all_connections
        for websocket in websockets_to_close:
            try:
                # Prepare the close message as a JSON string
                close_message = json.dumps({"type": "close_connection", "message": "Connection closed by server"})
                # Send the close message to the client
                await websocket.send(close_message)  # Make sure to await the send operation
                # Optionally, wait for a response or a specific condition before closing, if needed

                # Close the websocket connection
                await websocket.close()

                logging.info(f"Sent close_connection message and closed websocket: {websocket}")
            except Exception as e:
                logging.error(f"Error attempting `safe` websocket close: {e}")

            # Remove the websocket from the tracking set
            self.all_connections.discard(websocket)

    async def add_registered_connection(self, token, websocket):
        # async with self.connections_lock:
        self.registered_connections[token] = websocket
        await update_connection_status(token, 1)

    async def add_connection_mapping(
            self, master_token, connection_token, name, description
    ):
        # async with self.connections_lock:
        await add_connection_mapping(master_token, connection_token, name, description)

    async def remove_connection(self, token):
        # async with self.connections_lock:
        if token in self.registered_connections:
            self.all_connections.discard(self.registered_connections[token])
            del self.registered_connections[token]
            await update_connection_status(token, 0)

    async def isWebSocketOrphaned(self, search_websocket):
        """
        Check if a given websocket is orphaned (not associated with any token).

        :param search_websocket: The websocket instance to check.
        :return: True if the websocket is not associated with any token, False otherwise.
        """
        return not any(websocket == search_websocket for websocket in self.registered_connections.values())

    async def check_client_health(self):
        # async with self.connections_lock:
        disconnected_tokens = []
        print("************* CONNECTIONS START ****************")
        for token, websocket in self.registered_connections.items():
            print("CONNECTIONS-START:" + str(token) + ":" + str(websocket))
            try:
                await websocket.ping()
            except websockets.exceptions.ConnectionClosed:
                disconnected_tokens.append(token)
        print("************* CONNECTIONS END ******************")

        for token in disconnected_tokens:
            await self.remove_connection(token)

    async def get_websocket(self, token):
        # async with self.connections_lock:
        return self.registered_connections.get(token)

    async def send_message_to_token(self, token: str, message_id: str, message: str):
        websocket = await self.get_websocket(token)
        if not websocket:
            print(f"No active connection for token: {token}")
            return False
        try:
            # inject message_id into message
            message["message_id"] = message_id

            json_message = json.dumps(message)

            await websocket.send(json_message)

            return True
        except websockets.exceptions.ConnectionClosed:
            await self.remove_connection(token)
            return False
