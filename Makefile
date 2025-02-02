U := uv run
UM := uv run manage.py

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
	tree -I 'templates|__pycache__|*.pyc|db.sqlite3|asgi.py|wsgi.py|Makefile|pyproject.toml|uv.lock|README.md' .

rls:
	@$(U) python hexlet-code/manage.py runserver

# \
Cannot have hexlet-code in path because of hyphen - in package name \
So hexlet-code is not a valid Python identifier, so Python cannot resolve it as a package \
rps: \
	python -m gunicorn hexlet-code.task_manager.wsgi \
#

s:
	@$(UM) shell_plus --ipython

m: 
	@$(UM) migrate

ts:
	@$(U) pytest .

l:
	@$(U) ruff check hexlet-code