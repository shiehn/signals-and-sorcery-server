import json
from uuid import uuid4

import aiohttp
import asyncio

from dawnet_discovery_server.config import CONFIG



async def create_compute_contract(token: str, data):
    dict_data = data.to_dict()
    print('dict_data: ' + str(dict_data))

    json_data = {
        'id': token,
        'data': dict_data,
    }
    print('PAYLOAD SENDING: ', json_data)

    max_retries = 3  # Maximum number of retries
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(CONFIG['URL_BASE'] + CONFIG['URL_CREATE_COMPUTE_CONTRACT'],
                                        json=json_data) as response:
                    response_data = await response.text()
                    if response.status != 200:
                        print(
                            f"Error creating compute contract. Status code: {response.status}, Response: {response_data}")
                    else:
                        print(f"Successfully created compute contract. Response: {response_data}")
                        return response_data  # Successful response, exit the function
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise  # Re-raise the last exception if all retries fail

        # TODO: MOVE THIS TO BYOC_API.PY


async def update_connection_status(token: str, status: int):
    update_url = CONFIG['URL_BASE'] + CONFIG['URL_UPDATE_CONNECTION_STATUS'].format(token=token,
                                                                                    connection_status=status)

    max_retries = 3  # Define the maximum number of retries
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(update_url) as response:
                    if response.status != 200:
                        print(f"Error updating status for client_id: {token}. Status code: {response.status}")
                    else:
                        print(f"Successfully updated status for client_id: {token}")
                        return  # Exit the function on successful response
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise  # Re-raise the last exception if all retries fail


# TODO: MOVE THIS TO BYOC_API.PY
async def update_message_status(token: str, message_id: str, new_status: str):
    update_url = CONFIG['URL_BASE'] + CONFIG['URL_UPDATE_MESSAGE_STATUS'].format(token=token, message_id=message_id)
    payload = {'status': new_status}

    max_retries = 3  # Define the maximum number of retries
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(update_url, json=payload) as response:
                    response_data = await response.text()
                    print("UPDATE RES: " + str(response_data))
                    if response.status != 200:
                        print(
                            f"Error updating status for message_id: {message_id} with token: {token}. Status code: {response.status}, Response: {response_data}")
                    else:
                        print(
                            f"Successfully updated status for message_id: {message_id} with token: {token}. Response: {response_data}")
                        return  # Exit the function on successful response
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise  # Re-raise the last exception if all retries fail


async def send_message_response(token: str, message_id: str, response: str):
    send_response_url = CONFIG['URL_BASE'] + CONFIG['URL_SEND_MESSAGE_RESPONSE']

    payload = {
        'id': message_id,
        'token': token,
        'response': response,
        'status': 'completed'
    }

    max_retries = 3  # Define the maximum number of retries
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(send_response_url, json=payload) as response:
                    response_data = await response.text()
                    print("SEND_RESPONSE_STATUS: " + str(response_data))
                    if response.status != 200:
                        print(
                            f"Error responding to message_id: {message_id} with token: {token}. Status code: {response.status}, Response: {response_data}")
                    else:
                        print(
                            f"Successfully responded to message_id: {message_id} with token: {token}. Response: {response_data}")
                        return response_data  # Break out of the loop on success
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:  # Check if we've reached the max retries
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise  # Re-raise the last exception if all retries fail
