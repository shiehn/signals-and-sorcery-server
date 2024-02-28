import subprocess
import sys
import uuid
import subprocess
import time
import requests

from dawnet_api import register_the_plugin_token, get_connection_mappings, fetch_contract, send_request, \
    get_message_responses


def start_service():
    print(f"File Transfer Test Started for token: {token}")

    # Start service.py as a subprocess
    return subprocess.Popen(['python', 'dawnet_remote_a.py', token])


def stop_service(process):
    # Terminate the subprocess
    process.terminate()
    process.wait()

    print(f"File Transfer Test Completed for token: {token}")


def health_check(url):
    # Implement a simple health check by querying the service's root or a specific endpoint.
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def main():
    service_process = 0
    try:
        register_the_plugin_token(token)

        service_process = start_service()

        connection_mappings = []
        print("Waiting for connected remotes")
        while not get_connection_mappings(token):
            time.sleep(1)  # Wait a bit before trying again

        # [{'id': '9connection_mappingsc81ed92-c08c-4d05-9293-f357d51721e4',
        #   'master_token': '4ad34c17-7c88-407f-8021-984054aa32dd',
        #   'connection_token': 'a84f8256-791e-5b6e-84ab-921637113a16',
        #   'connection_name': 'DAWNet Template',
        #   'description': 'This is a template intended as a starting place to create custom DAWNet functions.',
        #   'created_at': '2024-02-27T19:44:10',
        #   'updated_at': '2024-02-27T19:44:10'}]

        print("Service is up!")
        connection_mapping = get_connection_mappings(token)[0]
        # print("MAPPINGS: " + str(connection_mapping))
        print("MASTER_TOKEN: " + connection_mapping['master_token'])
        print("CONNECTION_TOKEN: " + connection_mapping['connection_token'])
        print("CONNECTION_NAME: " + connection_mapping['connection_name'])

        connection_token = connection_mapping['connection_token']

        contract = fetch_contract(connection_token)

        print("CONTRACT: " + str(contract))

        # CONTRACT: {'id': '243348dc-6c7d-53ca-a766-8c5033c53ff6',
        # 'data': {'name': 'DAWNet Template', 'author': 'Default Author',
        # 'params': [
        # {'max': 10, 'min': 0, 'name': 'a', 'step': 1, 'type': 'int', 'options': [], 'ui_component': 'DAWNetNumberSlider', 'default_value': 5},
        # {'max': 0, 'min': 0, 'name': 'b', 'step': 0, 'type': 'DAWNetFilePath', 'options': [], 'ui_component': None, 'default_value': None},
        # {'max': 0, 'min': 0, 'name': 'c', 'step': 0, 'type': 'bool', 'options': [], 'ui_component': None, 'default_value': False}],
        # 'version': '0.0.0',
        # 'description': 'This is a template intended as a starting place to create custom DAWNet functions.',
        # 'method_name': 'arbitrary_method'},
        # 'created_at': '2024-02-27T20:35:55',
        # 'updated_at': '2024-02-27T20:35:55'}

        # time.sleep(10)

        # *************** SEND REQUEST ******************

        import json

        # Example usage
        token_value = connection_token
        input_file_url = "https://storage.googleapis.com/byoc-file-transfer/test_16_44100_stereo.aif"

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

        print("MESSAGE_ID: " + str(message_id))

        responses = {}
        while 'response' not in responses or responses['response'] is None:
            responses = get_message_responses(message_id, connection_token)
            print("MESSAGE_NONE_RESPONSES: " + str(responses))
            time.sleep(2)

        if 'files' in responses['response'] and responses['response']['files'] is not None:
            stop_service(service_process)
            print("SUCCESS! FILE_FOUND:" + str(responses['response']['files']))

        else:
            stop_service(service_process)
            raise Exception("FILE NOT RETURNED")


        # RESPONSE 1
        # {'id': '705becd5-6f70-4c3b-96b2-f8a312254101',
        # 'token': 'c777e9a6-d13c-5230-bf1c-6e71d98bc843',
        # 'request': {'bpm': 0, 'data': {
        # 'params': {'input_file': {
        # 'type': 'DAWNetFilePath',
        # 'value': 'https://storage.googleapis.com/byoc-file-transfer/test_16_44100_stereo.aif'}},
        # 'method_name': 'arbitrary_method'},
        # 'type': 'run_method',
        # 'token': 'c777e9a6-d13c-5230-bf1c-6e71d98bc843', 'sample_rate': 0},
        # 'response': None, 'status': 'pending', 'created_at': '2024-02-28T00:16:01', 'updated_at': '2024-02-28T00:16:01'}

        # RESPONSE 2
        # {'id': '705becd5-6f70-4c3b-96b2-f8a312254101',
        # 'token': 'c777e9a6-d13c-5230-bf1c-6e71d98bc843',
        # 'request': {'bpm': 0,
        # 'data': {
        # 'params': {
        # 'input_file': {
        # 'type': 'DAWNetFilePath',
        # 'value': 'https://storage.googleapis.com/byoc-file-transfer/test_16_44100_stereo.aif'
        # }
        #  },
        # 'method_name': 'arbitrary_method'
        # },
        # 'type': 'run_method',
        # 'token': 'c777e9a6-d13c-5230-bf1c-6e71d98bc843', 'sample_rate': 0},
        # 'response': {'logs': 'Input File: /tmp/tmpv17ig4qe/resampled/test_16_44100_stereo.wav\n',
        # 'error': None, 'files': [{'url': 'https://storage.googleapis.com/byoc-file-transfer/test_16_44100_stereo.wav',
        # 'name': 'test_16_44100_stereo.wav', 'type': 'unknown'}], 'message': 'This is a message send to the plugin'},
        # 'status': 'completed', 'created_at': '2024-02-28T00:16:01', 'updated_at': '2024-02-28T00:16:07'}

        # {
        #     "token": "3bac1fe8-f365-5e94-8096-de559931ffb1",
        #     "request": {
        #         "token": "3bac1fe8-f365-5e94-8096-de559931ffb1",
        #         "type": "run_method",
        #         "bpm": 0,
        #         "sample_rate": 0,
        #         "data": {
        #             "method_name": "dawnet_func",
        #             "params": {
        #                 "input_file": {
        #                     "value": "https://storage.googleapis.com/byoc-file-transfer/test_16_44100_stereo.aif",
        #                     "type": "DAWNetFilePath"
        #                 }
        #             }
        #         }
        #     }
        # }

        # Perform your tests here (example HTTP request)
        # try:
        #     response = requests.get(service_url)
        #     if response.status_code == 200:
        #         print("Test Successful: ", response.text)
        #     else:
        #         print("Test Failed with status code: ", response.status_code)
        # except Exception as e:
        #     print("An error occurred during the test: ", e)
    except Exception as e:
        stop_service(service_process)
        print("Service has been stopped.")
        raise Exception(f"ERROR: {e}")

    # Shutdown the service
    stop_service(service_process)
    print("Service has been stopped.")


token = str(uuid.uuid4())

if __name__ == '__main__':
    main()
