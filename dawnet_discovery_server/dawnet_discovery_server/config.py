import logging
import os
import configparser

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, "..", "config.ini")

parser = configparser.ConfigParser()
parser.read(config_path)

CONFIG = {
    "URL_BASE": os.getenv("DN_WS_URL_BASE", parser.get("DEFAULT", "URL_BASE")),
    "URL_UPDATE_CONNECTION_STATUS": os.getenv(
        "DN_WS_URL_UPDATE_CONNECTION_STATUS",
        parser.get("DEFAULT", "URL_UPDATE_CONNECTION_STATUS"),
    ),
    "URL_GET_CONNECTIONS": os.getenv(
        "DN_WS_URL_GET_CONNECTIONS", parser.get("DEFAULT", "URL_GET_CONNECTIONS")
    ),
    "URL_ADD_CONNECTION_MAPPING": os.getenv(
        "DN_WS_ADD_CONNECTION_MAPPING",
        parser.get("DEFAULT", "URL_ADD_CONNECTION_MAPPING"),
    ),
    "URL_CREATE_COMPUTE_CONTRACT": os.getenv(
        "DN_WS_URL_CREATE_COMPUTE_CONTRACT",
        parser.get("DEFAULT", "URL_CREATE_COMPUTE_CONTRACT"),
    ),
    "URL_GET_COMPUTE_CONTRACT": os.getenv(
        "DN_WS_URL_GET_COMPUTE_CONTRACT",
        parser.get("DEFAULT", "URL_GET_COMPUTE_CONTRACT"),
    ),
    "URL_GET_PENDING_MESSAGES": os.getenv(
        "DN_WS_URL_GET_PENDING_MESSAGES",
        parser.get("DEFAULT", "URL_GET_PENDING_MESSAGES"),
    ),
    "URL_UPDATE_MESSAGE_STATUS": os.getenv(
        "DN_WS_URL_UPDATE_MESSAGE_STATUS",
        parser.get("DEFAULT", "URL_UPDATE_MESSAGE_STATUS"),
    ),
    "URL_SEND_MESSAGE_RESPONSE": os.getenv(
        "DN_WS_URL_SEND_MESSAGE_RESPONSE",
        parser.get("DEFAULT", "URL_SEND_MESSAGE_RESPONSE"),
    ),
    "IP": os.getenv("DN_WS_IP", parser.get("DEFAULT", "IP")),
    "PORT": int(os.getenv("DN_WS_PORT", parser.get("DEFAULT", "PORT"))),
    "SLEEP_TIME": int(
        os.getenv("DN_WS_SLEEP_TIME", parser.get("DEFAULT", "SLEEP_TIME"))
    ),
    "FETCH_PENDING_REQUESTS_INTERVAL": int(
        os.getenv(
            "DN_WS_FETCH_PENDING_REQUESTS_INTERVAL",
            parser.get("DEFAULT", "FETCH_PENDING_REQUESTS_INTERVAL"),
        )
    ),
    "CLIENT_SOCKET_HEALTH_CHECK_INTERVAL": int(
        os.getenv(
            "DN_WS_CLIENT_SOCKET_HEALTH_CHECK_INTERVAL",
            parser.get("DEFAULT", "CLIENT_SOCKET_HEALTH_CHECK_INTERVAL"),
        )
    ),
}
