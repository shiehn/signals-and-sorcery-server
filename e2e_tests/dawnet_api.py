# BASE_URL = 'http://34.135.228.111:8081/api/hub/healthcheck/'
from urllib.parse import quote

# export const API_URLS = {
#                         //MASTER TOKEN MAPPING
# ADD_CONNECTION_MAPPING: (apiBaseUrl) => `${formatBaseUrl(apiBaseUrl)}/api/hub/connection_mappings/`,
# GET_CONNECTION_MAPPINGS: (apiBaseUrl, masterToken) => `${formatBaseUrl(apiBaseUrl)}/api/hub/connection_mappings/${masterToken}/`,
# REMOVE_CONNECTION_MAPPING: (apiBaseUrl, masterToken, connectionToken) => `${formatBaseUrl(apiBaseUrl)}/api/hub/connection_mappings/${masterToken}/${connectionToken}/`,
#
# //REMOTE CONNECTIONS
# PLUGIN_CONNECTION: (apiBaseUrl, token, status) => `${formatBaseUrl(apiBaseUrl)}/api/hub/connection/plugin/${token}/${status}/`,
# CONNECTION_STATUS: (apiBaseUrl, uuid) => `${formatBaseUrl(apiBaseUrl)}/api/hub/connections/${uuid}/`,
# COMPUTE_CONTRACT: (apiBaseUrl, uuid) => `${formatBaseUrl(apiBaseUrl)}/api/hub/compute/contract/${uuid}/`,
#
# //MESSAGE API
# MESSAGE_SEND: (apiBaseUrl) => `${formatBaseUrl(apiBaseUrl)}/api/hub/send_message/`,
# MESSAGE_SEND_RESPONSE: (apiBaseUrl) => `${formatBaseUrl(apiBaseUrl)}/api/hub/reply_to_message/`,
# MESSAGE_ABORT: (apiBaseUrl, token) => `${formatBaseUrl(apiBaseUrl)}/api/hub/abort_messages/${token}/`,
# MESSAGE_RESPONSES: (apiBaseUrl, message_id, token) => `${formatBaseUrl(apiBaseUrl)}/api/hub/get_response/${message_id}/${token}/`,
#
# //GCP STORAGE
# STORAGE_GET_SIGNED_URL: (apiBaseUrl, filename, token) => `${formatBaseUrl(apiBaseUrl)}/api/hub/get_signed_url/?token=${token}&filename=${encodeURIComponent(filename)}`,
# };


import requests

BASE_URL = 'http://34.135.228.111:8081'


def API_URLS_PLUGIN_CONNECTION(token: str):
    status = 1
    return f"{BASE_URL}/api/plugin_connection?token={token}&status={status}"


def API_URLS_GET_CONNECTION_MAPPINGS(token: str):
    return f"{BASE_URL}/api/hub/connection_mappings/{token}/"


def API_URLS_COMPUTE_CONTRACT(connection_token: str):
    # COMPUTE_CONTRACT: (apiBaseUrl, uuid) => `${formatBaseUrl(apiBaseUrl)}/api/hub/compute/contract/${uuid}/`,
    return f"{BASE_URL}/api/hub/compute/contract/{connection_token}/"


def API_URLS_SEND_MESSAGE():
    url = f"{BASE_URL}/api/hub/send_message/"
    return url


def API_MESSAGE_RESPONSES(message_id: str, token: str):
    return f"{BASE_URL}/api/hub/get_response/{message_id}/{token}/"


def API_GET_SIGNED_UPLOAD_URL(token: str, filename: str):
    return f"{BASE_URL}/api/hub/get_signed_url/?token={token}&filename=${quote(filename, safe='')}"


def register_the_plugin_token(token):
    if not token:
        return

    url = API_URLS_PLUGIN_CONNECTION(token)

    try:
        response = requests.put(url, json={'status': 1}, headers={'Content-Type': 'application/json'})

        if response.status_code != 200:
            raise Exception('Plugin connection status update failed')

        status_data = response.json()
        if status_data.get('success'):
            # Your success logic here (e.g., stopping an interval in JavaScript)
            pass
    except Exception as error:
        print(f"Error updating plugin connection status: {error}")


import requests


def get_connection_mappings(token: str):
    url = API_URLS_GET_CONNECTION_MAPPINGS(token)

    try:
        response = requests.get(url, allow_redirects=True)  # 'allow_redirects=True' is default and follows redirects

        if response.status_code == 200:
            return response.json()
        else:
            # Handle the error case, perhaps log it or use a Python equivalent of your toast error notification
            print('Error fetching connection mappings')
            return []
    except Exception as error:
        # Handle exceptions and log or notify as appropriate
        print(f'Error fetching connection mappings: {error}')
        return []


def fetch_contract(connection_token: str):
    url = API_URLS_COMPUTE_CONTRACT(connection_token)

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch contract data")
    except Exception as error:
        print(f"Error fetching contract: {error}")


def send_request(formatted_request_body):
    url = API_URLS_SEND_MESSAGE()

    try:
        response = requests.post(url, json=formatted_request_body, headers={'Content-Type': 'application/json'})

        if response.status_code != 201:
            print("RESPONSE ERROR: " + str(response))
            return

        response_data = response.json()
        message_id = response_data.get('id')
        return message_id
    except Exception as error:
        print(f"Error in network request: {error}")


def get_message_responses(message_id: str, token: str):
    url = API_MESSAGE_RESPONSES(message_id, token)

    try:
        response = requests.get(url, allow_redirects=True)  # 'allow_redirects=True' is default and follows redirects

        if response.status_code == 200:
            return response.json()
        else:
            # Handle the error case, perhaps log it or use a Python equivalent of your toast error notification
            print('Error fetching message responses')
            return []
    except Exception as error:
        # Handle exceptions and log or notify as appropriate
        print(f'Error fetching message responses: {error}')
        return []


def get_message_responses(message_id: str, token: str):
    url = API_MESSAGE_RESPONSES(message_id, token)

    try:
        response = requests.get(url, allow_redirects=True)  # 'allow_redirects=True' is default and follows redirects

        if response.status_code == 200:
            return response.json()
        else:
            # Handle the error case, perhaps log it or use a Python equivalent of your toast error notification
            print('Error fetching message responses')
            return []
    except Exception as error:
        # Handle exceptions and log or notify as appropriate
        print(f'Error fetching message responses: {error}')
        return []


def get_signed_upload_url(token: str, filename: str):
    url = API_GET_SIGNED_UPLOAD_URL(token, filename)

    try:
        response = requests.get(url, allow_redirects=True)

        if response.status_code == 200:
            return response.json()['signed_url']
        else:
            raise Exception(f"UNABLE TO GET UPLOAD URL for token={token} and filename={filename}")
    except Exception as error:
        raise Exception(f"UNABLE TO GET UPLOAD URL for token={token} and filename={filename}")


def upload_file_to_gcp(file_path, signed_url, content_type):
    try:
        with open(file_path, 'rb') as file:
            headers = {'Content-Type': content_type}
            response = requests.put(signed_url, data=file, headers=headers)

        if response.ok:
            print("File successfully uploaded to GCP Storage.")
        else:
            raise Exception(
                f"File upload to GCP Storage failed. Status: {response.status_code}, Message: {response.text}")
    except Exception as error:
        raise Exception(f"Error during file upload to GCP Storage: {error}")

# async function getSignedUrl(file) {
#
#     const tempFileToUpload = createTestFile();
#     const {connection_token, server_ip} = useStore();
#
#     // Fetch the signed URL from your DRF API with the custom token in the header
#     const response = await fetch(API_URLS.STORAGE_GET_SIGNED_URL(server_ip,file.name, connection_token), {
#     method: 'GET',
#     headers: {
#         'Content-Type': 'application/json',
#     }
#     });
#
#
#     //todo - check if response is ok
#     const data = await response.json();
#     const signedUrl = data.signed_url;
#
#     return signedUrl;
# }

# CONTRACT:
#
# {
#     "id": "3bac1fe8-f365-5e94-8096-de559931ffb1",
#     "data": {
#         "name": "DAWNet Template",
#         "author": "Default Author",
#         "params": [
#             {
#                 "max": 0,
#                 "min": 0,
#                 "name": "input_file",
#                 "step": 0,
#                 "type": "DAWNetFilePath",
#                 "options": [],
#                 "ui_component": null,
#                 "default_value": null
#             }
#         ],
#         "version": "0.0.0",
#         "description": "This is a template for creati
# FORM_DATA:
#
# {
#     "input_file": {
#         "type": "str",
#         "value": "https://storage.googleapis.com/byoc-file-transfer/test_16_44100_stereo.aif"
#     }
# }
#
# FORMATTED_REQUEST:
#
# {
#     "token": "3bac1fe8-f365-5e94-8096-de559931ffb1",
#     "request": {
#         "token": "3bac1fe8-f365-5e94-8096-de559931ffb1",
#         "type": "run_method",
#         "bpm": 0,
#         "sample_rate": 0,

#         "data": {


#             "params": {
#                 "input_file": {
#                     "value": "https://storage.googleapis.com/byoc-file-transfer/test_16_44100_stereo.aif",
#                     "type": "DAWNetFilePath"
#                 }
#             }
#         }
#     }
# }
