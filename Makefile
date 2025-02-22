U := uv run
UP := $(U) python
UM := $(UP) manage.py

build:
	./build.sh

install:
	uv pip install .

# The project's requirements disallow using static files
collectstatic:

migrate:
	@$(UM) migrate

render-start:
	python -m gunicorn task_manager.wsgi

t:
	tree -I 'db.sqlite3|00*|build|project_4.egg-info|templates|__pycache__|*.pyc|asgi.py|wsgi.py|Makefile|pyproject.toml|uv.lock|README.md|env|build.sh' .

rls:
	@$(UM) runserver

rgs:
	@$(UP) -m gunicorn --reload task_manager.wsgi

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