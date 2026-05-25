mkdir log -p
source .venv/bin/activate
gunicorn -c gunicorn.conf.py main:app -D
