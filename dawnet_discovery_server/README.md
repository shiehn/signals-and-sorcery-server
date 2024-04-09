

LOCAL TEST:

`pip uninstall dawnet_discovery_server -y && pip install . && python ./start_server.py`


ENVIRONMENT VARIABLES:

- "DN_TIMEOUT_CONNECTION_INTERVAL" Times out connects from plugin and client (default: 20 seconds)
- "DN_EXPIRE_CONNECTION_INTERVAL" Removes connections records from the server (default: 3600 seconds)