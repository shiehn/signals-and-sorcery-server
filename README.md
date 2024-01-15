# Django Seed

The purpose of this repository is just to share a homemade seed to create an API and CMS in Python 3, Django and Django Rest Framework.

You can setup this project with a Docker and manually.

## Manual Installation

Requires [Python 3.9](https://www.python.org/downloads/) and [Postgresql 13+](https://www.postgresql.org/download/)

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

### Run

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

The server will be ready on http://localhost:8080.

## Automatic Installation

Requires [Docker 20+](https://docs.docker.com/get-docker/) and [Docker Compose 1+](https://docs.docker.com/compose/install/)

```bash
docker-compose up --build
````

### Run

As explained above, you have two different settings you can launch, with docker both of them will be ready on:

 * api: `http://localhost:8081`
 * cms: `http://localhost:8082`

## CMS

To be able to access the CMS, you'll have to create a super user beforehand with the command:

```bash
make setting=web superuser
````

## API

### Swagger

To see the API swagger, you must launch the server.

```bash
make install
make setting=api server
```

Then goes on this URL `http://127.0.0.1:8080/api/swagger`.

You can check the validity of the swagger by installing `swagger-cli` through the command:
```bash
npm install -g swagger-cli
```
Then you can launch the command:
```bash
make setting=api swagger-check
```

### Test

You can test the API by launching this command:
```bash
make setting=api app=api test_app
```

## Code linting
```bash
make lint
```

In order to enforce a certain code quality, the option `--fail-under` is used, and is configured to fail if the score is below 9.0 (see Makefile).

Before each Pull Request, we expect developers to run this command and fix most of errors or warnings displayed.

After creating a new module, it has to be added into the Makefile command.

As part of the linting, be aware you have to use [typings](https://docs.python.org/3/library/typing.html) in all the code you're creating.

## Other commands

### Super User creation

```bash
make settings=xxx superuser
```

### Greenkeeping

```bash
make greenkeeping
```

Then run the tests, as explained above, to verify nothing has been broken.

## i18N

The translation files (po) are in locale/<lang>/LC_MESSAGES/django.po.

### To generate them:

```bash
make setting=web makemessages
```

The setup is at the bottom of the app/settings.py.

The way to use it is:

In python code:

```python
from django.utils.translation import gettext_lazy as _

return JsonResponse({'message': _('NoFortune')}, status=404)
```

In template:

```html
{% load i18n %}
<p>{% trans 'YourFortune' %}</p>
```

### To compile the messages (so that Django can use them) run:

```bash
make setting=web compilemessages
```

Note for the ops: the compiled files won't be kept in git, so they have to be re-generated at every deployment.

### API Example:

```bash
➜  django-seed git:(master) ✗ curl http://localhost:8080/sample/
{"message": "Success"}

➜  django-seed git:(master) ✗ curl http://localhost:8080/sample/ -H 'Accept-Language: fr'
{"message": "Succès"}
```

## OPS

## Celery

There is a Celery project embedded in this django project and it can be found in the following files:

 * app/__init__.py (imports the Celery config file)
 * app/main_celery.py (Celery config)
 * tasks/tasks.py (list of tasks)

### Run the server

```bash
make setting=api celery
```

### Tasks

In order to use your task (decorated with `@shared_task`), launch the celery server and in another console you can do the following:
```bash
make setting=api shell
from tasks.tasks import test
test.delay({'test': 'abc', 'true': 'yes'})
```

## Environment variables

| Name                          | Type    | Default                                      | Description                                                                                      |
| ----------------------------- | ------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| DEBUG                         | Boolean | True                                         | Should be False in production                                                                    |
| POSTGRESQL_ADDON_DB           | String  | base                                         | Name of the psql database                                                                        |
| POSTGRESQL_ADDON_USER         | String  | base                                         | Name of the psql user                                                                            |
| POSTGRESQL_ADDON_PASSWORD     | String  | base                                         | Password of the psql user                                                                        |
| POSTGRESQL_ADDON_HOST         | String  | localhost                                    | Domain/Ip of the psql database                                                                   |
| POSTGRESQL_ADDON_PORT         | Integer | 5432                                         | Port of the psql database                                                                        |
| SENTRY_DSN                    | String  | X                                            | Sentry's DSN (will only be enabled if the DEBUG flag is FALSE)                                   |
| CELERY_QUEUE                  | String  | celery                                       | Name of the default celery queue                                                                 |
| REDIS_URL                     | String  | redis://localhost:6379/0                     | Redis URL used by Celery                                                                         |
