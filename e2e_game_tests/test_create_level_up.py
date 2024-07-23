# e2e_game_tests/test_api.py
import uuid
import requests
import time
import requests
from game_models.models import GameStates, GameMap
from game_engine.api.map_inspector import MapInspector

BASE_URL = "http://localhost:8081"

USER_ID = uuid.uuid4()

OPEN_AI_KEY = "xyz"


def wait_for_queue_status_completion(base_url, user_id, timeout=300, interval=10):
    start_time = time.time()

    while time.time() - start_time < timeout:
        response = requests.get(f"{base_url}/api/game-update-queue/{user_id}/")
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["user_id"] == str(user_id)

        if response_data["status"] == "completed":
            print("Queue status completed.")
            return response_data  # Return the final response data if needed
        else:
            print(f"Current status: {response_data['status']}. Waiting...")

        time.sleep(interval)

    raise TimeoutError(
        "The queue status did not change to 'completed' within the timeout period."
    )


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

    # FOURTH GENERATE ASSETS
    response = requests.post(
        f"{BASE_URL}/api/game-state/generate/assets/{USER_ID}/{OPEN_AI_KEY}/"
    )

    game_queue_update = wait_for_queue_status_completion(BASE_URL, USER_ID)

    assert game_queue_update["status"] == "completed"

    assert response.status_code == 200

    # FIFTH NOW, set the environment_id to the exit environment so level will work
    # game_state = GameStates.objects.get(user_id=USER_ID).first()
    # game_map = GameMap.objects.get(id=game_state.map_id).first()
    #
    # map_inspector = MapInspector(game_map.map_graph)
    #
    # exit_env_id = map_inspector.get_env_id_of_exit()
    # game_state.environment_id = exit_env_id
    # game_state.save()
    #
    # # SIXTH LEVEL UP
    # response = requests.get(f"{BASE_URL}/api/game-state/levelup/{exit_env_id}/")
    # assert response.status_code == 200
    #
    # # SEVENTH CONFIRM THAT THE GAME UPDATE QUEUE IS NOT EMPTY
    # response = requests.get(f"{BASE_URL}/api/game-update-queue/{USER_ID}/")
    # assert response.status_code == 200
    # assert response.json() == {"level": 1, "status": "queued", "user_id": str(USER_ID)}
    #
    # # EIGHTH GENERATE ASSETS FROM THE LEVEL UP
    # response = requests.post(
    #     f"{BASE_URL}/api/game-state/generate/assets/{USER_ID}/{OPEN_AI_KEY}/"
    # )
    #
    # game_queue_update = wait_for_queue_status_completion(BASE_URL, USER_ID)
    #
    # assert game_queue_update["status"] == "completed"
    #
    # assert response.statustatus_code == 200
