# DAWNet infrastructure (DockerCompose)

This is a monorepo containing all the services needed to support the DAWNet plugin and client.  The repo contains the following services:

* **DAWNET API SERVER:** The Django server (DRF) which serves the API and handles uploads/downloads to cloud storage.
* **DAWNET WEBSOCKET SERVER:** A Python websockets server which handles the realtime communication between the dawnet remote Google Colabs (or scripts)
* **POSTGRES DATABASE:** The database which stores all the data for the DAWNet infrastructure

NOTE: there are a few other services which are currently just placeholders to support potential functionality such as a web frontend for user auth, etc.

## Dependencies:

* **SERVER:** You will a server expose to the public internet.  I recommend a multi-core Ubuntu VM on AWS or GCP.
* **DOCKER-COMPOSE:** you will need docker and docker-compose installed on you server.  I recommend querying CHAT-GPT for instructions on how to install docker-compose on your server.
* **GCP CLOUD STORAGE:** As currently implemented the system expects to use GCP cloud storage for the storage of audio files.  You will need to create a GCP project and get a service key which is added as an environment variable to the docker-compose file.  See `example.env` for the required format of the service key.


## Running The Services

Set up your environment variables by copying `example.env` to `.env` and filling in the required values.

```bash
source ./your-env-file.env
````

Start the services using docker-compose:

```bash
docker-compose up --build
````
After running this command, (BY DEFAULT) you should have the following services exposed on the following ports:

* **DAWNET API SERVER:** `http://[YOUR-IP-AT-PORT]:8081`
* **DAWNET WEB SOCKET:** `http://[YOUR-IP-AT-PORT]:8765`

### NOTE:

Remember you'll need to expose your ports to the public internet on your VM.  (Query Chat-GPT for instructions on how to do this.)



