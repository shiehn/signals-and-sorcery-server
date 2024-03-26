# DAWNet

`DAWNet` is a DAW (digit audio workstation) plugin that connects to a remote Google Colab or Script.  A user can send audio files from the plugin for remote processing. Hence, perform computationally expensive tasks such as text-2-audio or stem separation without leaving the DAW. 

For more information:

- [https://dawnet.tools/](https://dawnet.tools/)

- [Community Discord](https://discord.gg/UcHCjfpRkV)


# DAWNet infrastructure (DockerCompose)

This is a monorepo containing all the services needed to support the DAWNet plugin and client.  The repo contains the following services:

* **DAWNET API SERVER:** The Django server (DRF) which serves the API and handles uploads/downloads to cloud storage.
* **DAWNET WEBSOCKET SERVER:** A Python websockets server which handles the realtime communication between the dawnet remote Google Colabs (or scripts)
* **POSTGRES DATABASE:** The database which stores all the data for the DAWNet infrastructure

NOTE: there are a few other services which are currently just placeholders to support potential functionality such as a web frontend for user auth, etc.

## MAKE COMMANDS

To install all dependencies:
```bash
make install
```

To delete all dependencies:
```bash
make clean
```

All the command from the Makefile would require to have your environment setup with the variables listed at the end of this file.
You may used `example.env` as a sample.

### DB MIGRATIONS

This django app has been setup for multi-settings mode (app/settings), two settings have been created:

* api
* web

There are inheriting everything from app/settings/base.py.

Here is an example of commands you can run for the `api` settings:


```bash
make setting=api migrations
make setting=api migrate
make setting=api port=8080 server
```

*note: migrations require you to have a virtual environment setup i.e:*
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
make setting=api migrations
```

The server will be ready on http://localhost:8080.


## Dependencies:

* **SERVER:** You will a server expose to the public internet.  I recommend a multi-core Ubuntu VM on AWS or GCP.
* **DOCKER-COMPOSE:** you will need docker and docker-compose installed on you server.  I recommend querying CHAT-GPT for instructions on how to install docker-compose on your server.
* **GCP CLOUD STORAGE:** As currently implemented the system expects to use GCP cloud storage for the storage and transfer of audio files.  You will need to create a GCP account, download the service account key, put it in the root of the repo, the filling the environment variables.  See `example.env` for the required format of the service key.


## Running The Services

Set up your environment variables by renaming the `example.env` to `.env` and fill in the required values.  

Start the services using docker-compose:

```bash
docker-compose up --build
````
After running this command, (BY DEFAULT) you should have the following services exposed on the following ports:

* **DAWNET API SERVER:** `http://[YOUR-IP-AT-PORT]:8081`
* **DAWNET WEB SOCKET:** `http://[YOUR-IP-AT-PORT]:8765`

### NOTE:

Remember you'll need to expose your ports to the public internet on your VM.  (Query Chat-GPT for instructions on how to do this.)

### NOTE:
When running migrations and dabase command make sure you are using the correct .env values.  Note: they will be different from outside docker. e.x

### Super User creation
```
make settings=xxx superuser
```

```
POSTGRESQL_ADDON_DB=
POSTGRESQL_ADDON_USER=
POSTGRESQL_ADDON_PASSWORD=
POSTGRESQL_ADDON_HOST=localhost
POSTGRESQL_ADDON_PORT=5438 (localport)
```



