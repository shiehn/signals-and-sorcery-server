import asyncio
import json

import websockets
import aiohttp

from .byoc_api import create_compute_contract, update_message_status, send_message_response
from .messages import create_message_from_json
from .config import CONFIG
from .connection_manager import ConnectionManager
from dawnet_client import SentryEventLogger, DNSystemType, DNTag, DNMsgStage

connection_manager = ConnectionManager()

dn_tracer = SentryEventLogger(service_name=DNSystemType.DN_DISCOVERY_SERVER.value)


async def fetch_pending_requests():
    while True:
        await asyncio.sleep(CONFIG['FETCH_PENDING_REQUESTS_INTERVAL'])
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(CONFIG['URL_BASE'] + CONFIG['URL_GET_PENDING_MESSAGES']) as response:
                    # Check response status. If not 200 OK, print error and continue.
                    if response.status != 200:
                        print(f"Error fetching connection statuses. HTTP status: {response.status}")
                        continue

                    # Try parsing the response to JSON
                    data = await response.json()

                    # print('LATEST_PENDING_MESSAGES: ', str(data))

                    # Loop through the connections and send the message to each one
                    for record in data:
                        print('ID: ', record['id'])
                        print('TOKEN: ', record['token'])
                        print('REQUEST: ', record['request'])
                        try:
                            result = await connection_manager.send_message_to_token(token=record['token'],
                                                                                    message_id=record['id'],
                                                                                    message=record['request'])

                            print("RESULT: " + str(result))

                            if result is True:
                                await update_message_status(token=record['token'],
                                                            message_id=record['id'],
                                                            new_status='processing')
                            else:
                                await update_message_status(token=record['token'],
                                                            message_id=record['id'],
                                                            new_status='error')
                        except Exception as e:
                            await update_message_status(token=record['token'],
                                                        message_id=record['id'], new_status='error')
                            print(f"Unexpected error during the forwarding of a pending request: {e}")

            except Exception as e:
                print(f"Unexpected error during check_connection_statuses: {e}")


async def send_trigger_periodically(websocket, client_id):
    while True:
        await asyncio.sleep(CONFIG['SLEEP_TIME'])
        await websocket.send("start_plugin")


async def server_handler(websocket, path):
    msg = None
    try:
        while True:
            raw_msg = await websocket.recv()

            try:
                msg = json.loads(raw_msg)
                if msg.get('type') == 'healthcheck':
                    await websocket.send(json.dumps({"status": "success"}))
                    continue
            except Exception as e:
                dn_tracer.log_error(str(msg.token), {
                    DNTag.DNMsgStage.value: DNMsgStage.WS_RECEIVE_MSG.value,
                    DNTag.DNMsg.value: str(e),
                })
                # Optionally send an error response back to the client
                await websocket.send(json.dumps({"status": "error", "reason": str(e)}))
                continue
            # HANDLE HEALTH CHECKS - START

            try:
                print("raw_msg: " + str(raw_msg))
                msg = create_message_from_json(raw_msg)
            except Exception as e:
                dn_tracer.log_error(str(msg.token), {
                    DNTag.DNMsgStage.value: DNMsgStage.WS_RECEIVE_MSG.value,
                    DNTag.DNMsg.value: str(e),
                })
                continue

            if str(msg.type) == 'register':
                # Add the connection to the ConnectionManager when a client connects
                print("MESSAGE: " + str(msg))
                try:
                    await connection_manager.add_connection(msg.token, websocket)
                    dn_tracer.log_event(str(msg.token), {
                        DNTag.DNMsgStage.value: DNMsgStage.WS_REG_TOKEN.value,
                        DNTag.DNMsg.value: "success",
                    })
                except Exception as e:
                    dn_tracer.log_error(str(msg.token), {
                        DNTag.DNMsgStage.value: DNMsgStage.WS_REG_TOKEN.value,
                        DNTag.DNMsg.value: str(e),
                    })
                    continue
            elif str(msg.type) == 'contract':
                try:
                    await create_compute_contract(msg.token, msg.data)
                    dn_tracer.log_event(str(msg.token), {
                        DNTag.DNMsgStage.value: DNMsgStage.WS_REG_CONTRACT.value,
                        DNTag.DNMsg.value: "success",
                    })
                except Exception as e:
                    dn_tracer.log_error(str(msg.token), {
                        DNTag.DNMsgStage.value: DNMsgStage.WS_REG_CONTRACT.value,
                        DNTag.DNMsg.value: str(e),
                    })
                    continue
            elif str(msg.type) == 'results':
                dict_data = msg.data.to_dict()
                try:
                    await send_message_response(str(msg.token), str(dict_data['id']), dict_data['response'])
                    dn_tracer.log_event(str(msg.token), {
                        DNTag.DNMsgStage.value: DNMsgStage.WS_SEND_RESULTS.value,
                        DNTag.DNMsg.value: "success",
                    })
                except Exception as e:
                    dn_tracer.log_error(str(msg.token), {
                        DNTag.DNMsgStage.value: DNMsgStage.WS_SEND_RESULTS.value,
                        DNTag.DNMsg.value: str(e),
                    })
                    continue

    except websockets.exceptions.ConnectionClosedOK:
        # Remove the connection when the client disconnects
        if msg is not None and 'token' in msg:
            token = msg['token']
            if token is not None:
                print(f"WebSocket connection closed for token {token}")
                try:
                    await connection_manager.remove_connection(token)
                    dn_tracer.log_event(str(msg.token), {
                        DNTag.DNMsgStage.value: DNMsgStage.WS_UN_REG_TOKEN.value,
                        DNTag.DNMsg.value: "success",
                    })
                except Exception as e:
                    dn_tracer.log_error(str(msg.token), {
                        DNTag.DNMsgStage.value: DNMsgStage.WS_UN_REG_TOKEN.value,
                        DNTag.DNMsg.value: str(e),
                    })
            else:
                print("WebSocket connection closed")
        else:
            print("WebSocket connection closed")
    except websockets.exceptions.ConnectionClosedError as e:
        # Remove the connection when the client disconnects
        print(f"ERROR: WebSocket connection closed with error: {e}")

    except Exception as e:
        # Remove the connection when the client disconnects
        if msg is not None and 'token' in msg:
            token = msg['token']
            if token is not None:
                print(f"ERROR: WebSocket connection closed for token {token}")
                try:
                    await connection_manager.remove_connection(token)
                    dn_tracer.log_event(str(msg.token), {
                        DNTag.DNMsgStage.value: DNMsgStage.WS_UN_REG_TOKEN.value,
                        DNTag.DNMsg.value: "success",
                    })
                except Exception as e:
                    dn_tracer.log_error(str(msg.token), {
                        DNTag.DNMsgStage.value: DNMsgStage.WS_UN_REG_TOKEN.value,
                        DNTag.DNMsg.value: str(e),
                    })
            else:
                print("ERROR: WebSocket connection closed")
        else:
            print(f"ERROR: WebSocket connection closed with error: {e}")


async def check_all_clients_health():
    while True:
        # Wait for a configured time interval between health checks
        await asyncio.sleep(CONFIG['CLIENT_SOCKET_HEALTH_CHECK_INTERVAL'])

        # Check the health of all clients
        await connection_manager.check_client_health()


async def run_forever():
    while True:
        try:
            # Starting the server
            start_server = websockets.serve(
                server_handler,
                '0.0.0.0',
                8765,
                ping_interval=90,
                ping_timeout=90,
                close_timeout=10
            )

            server = await start_server

            # Running the server
            print("WebSocket server started.")
            await server.wait_closed()

        except Exception as e:
            print(f"WebSocket server crashed with error: {e}. Restarting server...")

            # Optional: wait a short time before restarting
            #await asyncio.sleep(5)

# This function remains the same
def setup_tasks():
    asyncio.create_task(fetch_pending_requests())
    asyncio.create_task(check_all_clients_health())

def run():
    try:
        loop = asyncio.get_event_loop()

        # Schedule the setup of tasks and the server
        loop.call_soon(setup_tasks)
        loop.run_until_complete(run_forever())

    except Exception as e:
        print(f"Event loop crashed with error: {e}")
