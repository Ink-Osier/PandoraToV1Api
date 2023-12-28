# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim

# 设置工作目录为 /app
WORKDIR /app

# 将当前目录内容复制到位于 /app 的容器中
COPY . /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
# 设置工作进程数
ENV PROCESS_WORKERS=1
# 设置工作线程数
ENV PROCESS_THREADS=2

RUN chmod +x /app/start.sh

# 设置 pip 源为清华大学镜像
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装任何所需的依赖项
RUN pip install --no-cache-dir flask gunicorn requests Pillow flask-cors tiktoken

# 在容器启动时运行 Flask 应用
CMD ["/app/start.sh"]
