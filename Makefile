U := uv run
UP := uv run python
UM := uv run python hexlet-code/manage.py

build:
	./build.sh

install:
	uv pip install .

# The project's requirements disallow using static files
collectstatic:

migrate:
	python hexlet-code/manage.py migrate

render-start:
	cd hexlet-code && python -m gunicorn task_manager.wsgi && cd ..

t:
	tree -I 'build|project_4.egg-info|templates|__pycache__|*.pyc|asgi.py|wsgi.py|Makefile|pyproject.toml|uv.lock|README.md|env|build.sh' .

rls:
	@$(U) python hexlet-code/manage.py runserver

rgs:
	cd hexlet-code && python -m gunicorn --reload task_manager.wsgi && cd ..

# \
Cannot have hexlet-code in path because of hyphen - in package name \
So hexlet-code is not a valid Python identifier, so Python cannot resolve it as a package \
rps: \
	python -m gunicorn hexlet-code.task_manager.wsgi \
#

ts:
	@$(U) pytest .

l:
	@$(U) ruff check hexlet-code

lg:
	less hexlet-code/debug.log

cl-lg:
	truncate -s 0 hexlet-code/debug.log

m:
	@$(UM) makemigrations

m-m:
	@$(UM) migrate

db:
	@$(UM) dbshell