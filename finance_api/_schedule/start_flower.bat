@echo off
cd D:\er-yan\finance_api
rem celery -A _schedule.celery_app:celery_app flower --address=0.0.0.0 --port=5555 --broker=redis://:123654@47.99.219.51:6379/0
celery -A _schedule.celery_app:celery_app flower --address=127.0.0.1 --port=5555
rem --broker=redis://:123654@47.99.219.51:6379/0 --result-backend=redis://:123654@47.99.219.51:6379/1 --broker-connect-timeout=600 --broker-publish-timeout=600
rem --basic-auth=username:password
rem --broker=redis://:123654@47.99.219.51:6379/0
rem flower -A your_project_name --broker=redis://:password@47.99.219.51:6379/0
rem celery -A your_app worker \
rem --broker=redis://:password@host:port/0 \
rem --result-backend=redis://:password@host:port/1 \
rem --broker-transport-options="{'socket_connect_timeout': 10, 'socket_timeout': 20}" \
rem --result-backend-transport-options="{'socket_connect_timeout': 10, 'socket_timeout': 20}"