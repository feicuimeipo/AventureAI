import multiprocessing

# 是否开启debug模式
debug = True
# 访问地址
bind = "0.0.0.0:8000"
# 工作进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_connections = 1000
worker_class = 'gevent'
# 工作线程数
# threads = 5
# 超时时间
timeout = 30
# 保持连接超时时间
keepalive = 2
# 输出日志级别
loglevel = 'debug'
# 存放日志路径
pidfile = "log/gunicorn.pid"
# 存放日志路径
accesslog = "log/access.log"
# 存放日志路径
errorlog = "log/debug.log"
# gunicorn + apscheduler场景下，解决多worker运行定时任务重复执行的问题
preload_app = True