gunicorn -w 5 -b 0.0.0.0:5000 -t 120 main:app

# 后台运行
# gunicorn -c gunicorn.conf.py main:app -D
# nohup python -m gunicorn -w 5 -b 0.0.0.0:6000 -t 120 main:app > app.log 2>&1 &

# -D表示将gunicorn置于后台运行，可以通过tail -f access.log或者tail -f error.log查看记录的日志信息。
# gunicorn -w 4 -b 0.0.0.0:8080 --access-logfile access.log --error-logfile error.log main:app -D


# -c gunicorn.conf.py
# --max-requests-jitter 50
# --worker-tmp-dir /dev/shm
# --certfile=server.crt --keyfile=server.key
# --log-level debug
# --proxy-protocol
# --limit-request-line 8190
# --limit-request-fields 100

