t:
	tree -I 'templates|*pycache*|*.pyc|db.sqlite3|asgi.py|wsgi.py|Makefile|pyproject.toml|uv.lock|README.md' .

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

