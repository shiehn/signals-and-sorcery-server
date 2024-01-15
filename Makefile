# Define default value for port
port ?= 8080

all: install migrate lint server

server:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) . env/bin/activate && python3 manage.py runserver $(port)

clean:
	rm -rf env/

install:
	python3 -m venv env
	. env/bin/activate && python -m pip install --upgrade pip
	. env/bin/activate && pip install -r requirements.txt

migrate:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) . env/bin/activate && python3 manage.py migrate

migrations:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) . env/bin/activate && python3 manage.py makemigrations

superuser:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) . env/bin/activate && python3 manage.py createsuperuser

lint:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) . env/bin/activate && pylint --fail-under 9.0 --load-plugins pylint_django --disable=duplicate-code app/**.py common/**.py tasks/*.py user/**.py api/**.py

test:
	DJANGO_SETTINGS_MODULE=app.settings.${setting} . env/bin/activate && python3 manage.py test --pattern="test_*.py"

test_app:
	DJANGO_SETTINGS_MODULE=app.settings.${setting} . env/bin/activate && python3 manage.py test ${app} --pattern="test_*.py"

swagger-check:
	swagger-cli validate app/static/swagger/api.swagger.yml || echo 'You need to install swagger-cli first with npm'

makemessages:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) . env/bin/activate && python3 manage.py makemessages -l en --ignore env*
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) . env/bin/activate && python3 manage.py makemessages -l fr --ignore env*

compilemessages:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) . env/bin/activate && python3 manage.py compilemessages -l en -l fr --ignore env*

celery:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) . env/bin/activate && celery -A app worker -E

greenkeeping:
	. env/bin/activate && pur -r requirements.txt

shell:
	DJANGO_SETTINGS_MODULE=app.settings.$(setting) . env/bin/activate && python3 manage.py shell