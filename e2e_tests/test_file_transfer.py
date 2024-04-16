import logging
import mimetypes
import os
import uuid
import subprocess
import time
from pathlib import Path
import sys
import requests
import json
import datetime



from dawnet_api import register_the_plugin_token, get_connection_mappings, fetch_contract, send_request, \
    get_message_responses, get_signed_upload_url, upload_file_to_gcp


def start_service():
    print(f"File Transfer Test Started for token: {token}")
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_script_dir, 'dawnet_remote_a.py')
    return subprocess.Popen(['python', script_path, token])


def stop_service(process):
    process.terminate()
    process.wait()
    print(f"File Transfer Test Completed for token: {token}")


def health_check(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: script_name.py <upload_file_path>")
        sys.exit(1)

    global upload_filepath
    upload_filepath = Path(sys.argv[1])  # Set upload_filepath based on command line argument



    service_process = 0
    try:
        start_time = time.time()  # Capture the start time
        print(f"Test started for {upload_filepath} at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")

        register_the_plugin_token(token)

        service_process = start_service()

        connection_mappings = []

        while not get_connection_mappings(token):
            # Check if the loop has run for more than 60 seconds
            if time.time() - start_time > 60:
                raise TimeoutError("The operation has timed out after 60 seconds.")
            time.sleep(1)

        print("Service is up!")
        connection_mapping = get_connection_mappings(token)[0]

        connection_token = connection_mapping['connection_token']

        contract = fetch_contract(connection_token)

        print("CONTRACT: " + str(contract))

        print(f"Getting Signed URL for {upload_filepath} at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
        signed_url = get_signed_upload_url(connection_token, upload_filepath.name)
        print(f"Received Signed URL for {upload_filepath} at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")

        print(f"XXX:{signed_url}")

        mime_type, _ = mimetypes.guess_type(upload_filepath)
        print(f"Upload to GCP: {upload_filepath} at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
        upload_file_to_gcp(upload_filepath.absolute(), signed_url, mime_type)
        print(f"Finish upload to GCP: {upload_filepath} at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")

        # Example usage
        token_value = connection_token
        input_file_url = "https://storage.googleapis.com/byoc-file-transfer/" + upload_filepath.name

        data_dict = {
            "token": token_value,
            "request": {
                "token": token_value,
                "type": "run_method",
                "bpm": 0,
                "sample_rate": 0,
                "data": {
                    "method_name": "arbitrary_method",
                    "params": {
                        "input_file": {
                            "value": input_file_url,
                            "type": "DAWNetFilePath"
                        }
                    }
                }
            }
        }

        message_id = send_request(data_dict)

        start_time = time.time()  # Capture the start time
        responses = {}

        while 'response' not in responses or responses['response'] is None:
            # Check if the loop has run for more than 60 seconds
            if time.time() - start_time > 60:
                raise TimeoutError("The operation has timed out after 60 seconds.")

            responses = get_message_responses(message_id, connection_token)
            print("MESSAGE_NONE_RESPONSES: " + str(responses))
            time.sleep(2)

        if 'files' in responses['response'] and responses['response']['files'] is not None and responses['response']['files'][0]['url'] == input_file_url:
            stop_service(service_process)
            print("SUCCESS! FILE_FOUND:" + str(responses['response']['files']))

        else:
            stop_service(service_process)
            raise Exception("FILE NOT RETURNED")

    except Exception as e:
        stop_service(service_process)
        print("Service has been stopped.")
        # At the end of your main function, log the completion time
        logging.info(f"Test completed for {upload_filepath}. Duration: {time.time() - start_time} seconds")

        raise Exception(f"ERROR: {e}")

    # Shutdown the service
    stop_service(service_process)
    print(f"Test completed for {upload_filepath}. Duration: {time.time() - start_time} seconds")

    print("----------------------")
    print("TEST SUCCESS!!!!")
    print("----------------------")
    print("Service has been stopped.")


token = str(uuid.uuid4())

if __name__ == '__main__':
    main()
