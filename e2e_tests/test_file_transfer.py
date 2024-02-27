import subprocess
import sys
import uuid
import subprocess
import time
import requests

from dawnet_api import register_the_plugin_token


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
    service_url = 'http://localhost:8000'  # Assuming your service runs on this URL
    register_the_plugin_token(token)

    
    service_process = start_service()



    # Wait for the service to be up
    # print("Waiting for the service to be up...")
    # while not health_check(service_url):
    #     time.sleep(1)  # Wait a bit before trying again
    # print("Service is up!")

    time.sleep(10)


    # Perform your tests here (example HTTP request)
    # try:
    #     response = requests.get(service_url)
    #     if response.status_code == 200:
    #         print("Test Successful: ", response.text)
    #     else:
    #         print("Test Failed with status code: ", response.status_code)
    # except Exception as e:
    #     print("An error occurred during the test: ", e)

    # Shutdown the service
    stop_service(service_process)
    print("Service has been stopped.")


token = str(uuid.uuid4())

if __name__ == '__main__':
    main()

