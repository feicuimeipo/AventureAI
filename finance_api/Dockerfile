# 基于Python官方镜像
FROM python:3.9-slim
# 设置工作目录
WORKDIR /app
# 复制依赖文件并安装
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# 复制项目代码
COPY . /app
# 暴露端口
EXPOSE 8000
# 启动命令
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "your_flask_app:app"]