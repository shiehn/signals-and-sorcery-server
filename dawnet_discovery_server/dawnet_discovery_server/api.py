import json
import logging
from uuid import uuid4
from urllib.parse import urljoin

import aiohttp
import asyncio

from .config import CONFIG

URL_TIMEOUT_CONNECTIONS = "/api/hub/connections_timeout/"
URL_EXPIRE_CONNECTIONS = "/api/hub/connections_expiry/"


async def timeout_connections_endpoint() -> bool:
    timout_url = urljoin(CONFIG["URL_BASE"], URL_TIMEOUT_CONNECTIONS)
    logging.info(f"timeout_connections_endpoint: {timout_url}")
    max_retries = 3  # Maximum number of retries
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(timout_url) as response:
                    if response.status != 200:
                        print(
                            f"Error attempting to timeout_connections. Status code: {response.status}"
                        )
                        return False
                    else:
                        print(
                            f"Successfully called timeout_connections. Response: {response.status}"
                        )
                        return True
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(
                f"Compute Contract Attempt {attempt + 1} for endpoint: {timout_url} failed: {e}"
            )
            if attempt < max_retries - 1:
                await asyncio.sleep(2**attempt)  # Exponential backoff
            else:
                raise  # Re-raise the last exception if all retries fail


async def expire_connections_endpoint() -> bool:
    expire_url = urljoin(CONFIG["URL_BASE"], URL_EXPIRE_CONNECTIONS)
    logging.info(f"expire_connections_endpoint: {expire_url}")
    max_retries = 3  # Maximum number of retries
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(expire_url) as response:
                    if response.status != 200:
                        print(
                            f"Error attempting to expire_connections. Status code: {response.status}"
                        )
                        return False
                    else:
                        print(
                            f"Successfully called expire_connections. Response: {response.status}"
                        )
                        return True
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(
                f"Compute Contract Attempt {attempt + 1} for endpoint: {expire_url} failed: {e}"
            )
            if attempt < max_retries - 1:
                await asyncio.sleep(2**attempt)  # Exponential backoff
            else:
                raise  # Re-raise the last exception if all retries fail


# async def create_compute_contract(token: str, data):
#     dict_data = data.to_dict()
#
#     json_data = {
#         "id": token,
#         "data": dict_data,
#     }
#
#     max_retries = 3  # Maximum number of retries
#     for attempt in range(max_retries):
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(
#                     urljoin(CONFIG["URL_BASE"], CONFIG["URL_CREATE_COMPUTE_CONTRACT"]),
#                     json=json_data,
#                 ) as response:
#                     response_data = await response.text()
#                     if response.status != 200:
#                         print(
#                             f"Error creating compute contract. Status code: {response.status}, Response: {response_data}"
#                         )
#                     else:
#                         print(
#                             f"Successfully created compute contract. Response: {response_data}"
#                         )
#                         return response_data  # Successful response, exit the function
#         except (aiohttp.ClientError, asyncio.TimeoutError) as e:
#             logging.error(f"Compute Contract Attempt {attempt + 1} failed: {e}")
#             if attempt < max_retries - 1:
#                 await asyncio.sleep(2**attempt)  # Exponential backoff
#             else:
#                 raise  # Re-raise the last exception if all retries fail
#
#         # TODO: MOVE THIS TO BYOC_API.PY
#
#
# async def update_connection_status(token: str, status: int):
#     update_url = urljoin(
#         CONFIG["URL_BASE"],
#         CONFIG["URL_UPDATE_CONNECTION_STATUS"].format(
#             token=token, connection_status=status
#         ),
#     )
#
#     logging.info(f"update_connection_status: {update_url}")
#
#     max_retries = 3  # Define the maximum number of retries
#     for attempt in range(max_retries):
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.put(update_url) as response:
#                     if response.status != 200:
#                         logging.info(
#                             f"Error updating status for client_id: {token}. Status code: {response.status}"
#                         )
#                     else:
#                         logging.info(
#                             f"Successfully updated status for client_id: {token}"
#                         )
#                         return  # Exit the function on successful response
#         except (aiohttp.ClientError, asyncio.TimeoutError) as e:
#             logging.error(f"Update Connection Status Attempt {attempt + 1} failed: {e}")
#             if attempt < max_retries - 1:
#                 await asyncio.sleep(2**attempt)  # Exponential backoff
#             else:
#                 raise  # Re-raise the last exception if all retries fail
#
#
# async def add_connection_mapping(
#     master_token: str, connection_token: str, name: str, description: str
# ):
#     add_mapping_url = urljoin(CONFIG["URL_BASE"], CONFIG["URL_ADD_CONNECTION_MAPPING"])
#
#     payload = {
#         "master_token": master_token,
#         "connection_token": connection_token,
#         "connection_name": name,
#         "description": description,
#     }
#
#     max_retries = 3  # Define the maximum number of retries
#     for attempt in range(max_retries):
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(add_mapping_url, json=payload) as response:
#                     response_data = await response.text()
#                     print("ADD_MAPPING_RES: " + str(response_data))
#                     if response.status != 200:
#                         print(
#                             f"Error adding connection mapping. Status code: {response.status}, Response: {response_data}"
#                         )
#                     else:
#                         print(
#                             f"Successfully added connection mapping. Response: {response_data}"
#                         )
#                         return response_data  # Break out of the loop on success
#         except (aiohttp.ClientError, asyncio.TimeoutError) as e:
#             logging.error(f"Add Connection Mapping Attempt {attempt + 1} failed: {e}")
#             if attempt < max_retries - 1:  # Check if we've reached the max retries
#                 await asyncio.sleep(2**attempt)  # Exponential backoff
#             else:
#                 raise  # Re-raise the last exception if all retries fail
#
#
# # TODO: MOVE THIS TO BYOC_API.PY
# async def update_message_status(token: str, message_id: str, new_status: str):
#     update_url = urljoin(
#         CONFIG["URL_BASE"],
#         CONFIG["URL_UPDATE_MESSAGE_STATUS"].format(token=token, message_id=message_id),
#     )
#     payload = {"status": new_status}
#
#     max_retries = 3  # Define the maximum number of retries
#     for attempt in range(max_retries):
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.patch(update_url, json=payload) as response:
#                     response_data = await response.text()
#                     print("UPDATE RES: " + str(response_data))
#                     if response.status != 200:
#                         print(
#                             f"Error updating status for message_id: {message_id} with token: {token}. Status code: {response.status}, Response: {response_data}"
#                         )
#                     else:
#                         print(
#                             f"Successfully updated status for message_id: {message_id} with token: {token}. Response: {response_data}"
#                         )
#                         return  # Exit the function on successful response
#         except (aiohttp.ClientError, asyncio.TimeoutError) as e:
#             logging.error(f"Update Message Status Attempt {attempt + 1} failed: {e}")
#             if attempt < max_retries - 1:
#                 await asyncio.sleep(2**attempt)  # Exponential backoff
#             else:
#                 raise  # Re-raise the last exception if all retries fail
#
#
# async def send_message_response(token: str, message_id: str, response: str):
#     send_response_url = urljoin(CONFIG["URL_BASE"], CONFIG["URL_SEND_MESSAGE_RESPONSE"])
#
#     payload = {
#         "id": message_id,
#         "token": token,
#         "response": response,
#         "status": "completed",
#     }
#
#     max_retries = 3  # Define the maximum number of retries
#     for attempt in range(max_retries):
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(send_response_url, json=payload) as response:
#                     response_data = await response.text()
#                     print("SEND_RESPONSE_STATUS: " + str(response_data))
#                     if response.status != 200:
#                         print(
#                             f"Error responding to message_id: {message_id} with token: {token}. Status code: {response.status}, Response: {response_data}"
#                         )
#                     else:
#                         print(
#                             f"Successfully responded to message_id: {message_id} with token: {token}. Response: {response_data}"
#                         )
#                         return response_data  # Break out of the loop on success
#         except (aiohttp.ClientError, asyncio.TimeoutError) as e:
#             logging.error(f"Send Message Response Attempt {attempt + 1} failed: {e}")
#             if attempt < max_retries - 1:  # Check if we've reached the max retries
#                 await asyncio.sleep(2**attempt)  # Exponential backoff
#             else:
#                 raise  # Re-raise the last exception if all retries fail
