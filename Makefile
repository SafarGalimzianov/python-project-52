U := uv run
UP := uv run python
UM := uv run python task_manager/manage.py

build:
	./build.sh

install:
	uv pip install .

# The project's requirements disallow using static files
collectstatic:

migrate:
	python task_manager/manage.py migrate

render-start:
	cd task_manager && python -m gunicorn task_manager.wsgi && cd ..

t:
	tree -I 'db.sqlite3|00*|build|project_4.egg-info|templates|__pycache__|*.pyc|asgi.py|wsgi.py|Makefile|pyproject.toml|uv.lock|README.md|env|build.sh' .

rls:
	@$(U) python task_manager/manage.py runserver

rgs:
	cd task_manager && python -m gunicorn --reload task_manager.wsgi && cd ..

# \
Cannot have hexlet-code in path because of hyphen - in package name \
So hexlet-code is not a valid Python identifier, so Python cannot resolve it as a package \
rps: \
	python -m gunicorn hexlet-code.task_manager.wsgi \
#

ts:
	@$(UM) test

l:
	@$(U) ruff check task_manager

lg:
	less task_manager/debug.log

cl-lg:
	truncate -s 0 task_manager/debug.log

m:
	@$(UM) makemigrations

m-m:
	@$(UM) migrate

db:
	@$(UM) dbshell