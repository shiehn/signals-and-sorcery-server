# e2e_game_tests/test_api.py
import uuid

import requests

BASE_URL = "http://localhost:8081"

USER_ID = uuid.uuid4()

OPEN_AI_KEY = "xyz"


def test_game_creation_flow():
    """
    Test the game creation flow
    """

    # FIRST CONFIRM THAT THE GAME UPDATE QUEUE IS EMPTY
    response = requests.get(f"{BASE_URL}/api/game-update-queue/{USER_ID}/")
    assert response.status_code == 404

    # SECOND CREATE A NEW GAME
    response = requests.post(
        f"{BASE_URL}/api/game-state/create/{OPEN_AI_KEY}/",
        json={
            "user_id": str(USER_ID),
            "level": 1,
            "aesthetic": "fantasy",
            "map_id": str(uuid.UUID("00000000-0000-0000-0000-000000000000")),
            "environment_id": str(uuid.UUID("00000000-0000-0000-0000-000000000000")),
            "environment_img": "https://storage.googleapis.com/byoc-file-transfer/img_placeholder.png",
        },
    )

    if response.status_code != 201:
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

    assert response.status_code == 201
    assert response.json()["user_id"] == str(USER_ID)

    # THIRD CONFIRM THAT THE GAME UPDATE QUEUE IS NOT EMPTY
    response = requests.get(f"{BASE_URL}/api/game-update-queue/{USER_ID}/")
    assert response.status_code == 200
    assert response.json() == {"level": 1, "status": "queued", "user_id": str(USER_ID)}


# def test_api_endpoint_2():
#     response = requests.post(f"{BASE_URL}/api/endpoint_2/", json={"key": "value"})
#     assert response.status_code == 200
#     assert response.json() == {"expected": "response"}
#
# def test_api_calls_in_sequence():
#     # First API call
#     response1 = requests.post(f"{BASE_URL}/api/endpoint_1/", json={"key": "value"})
#     assert response1.status_code == 200
#     # Additional assertions for response1
#
#     # Second API call
#     response2 = requests.post(f"{BASE_URL}/api/endpoint_2/", json={"key": "value"})
#     assert response2.status_code == 200
#     # Additional assertions for response2
#
#     # Third API call
#     response3 = requests.post(f"{BASE_URL}/api/endpoint_3/", json={"key": "value"})
#     assert response3.status_code == 200
#     # Additional assertions for response3
#
#     # Fourth API call
#     response4 = requests.post(f"{BASE_URL}/api/endpoint_4/", json={"key": "value"})
#     assert response4.status_code == 200
#     # Additional assertions for response4
#
#     # Fifth API call
#     response5 = requests.post(f"{BASE_URL}/api/endpoint_5/", json={"key": "value"})
#     assert response5.status_code == 200
#     # Additional assertions for response5
