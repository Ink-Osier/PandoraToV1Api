# 基础阶段，适用于所有平台
FROM python:3.9-slim AS base

WORKDIR /app

COPY . /app

ENV PYTHONUNBUFFERED=1

RUN chmod +x /app/start.sh

RUN apt update && apt install -y jq

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 针对 linux/amd64 和 linux/arm64 的阶段
FROM base AS amd64_arm64

# 针对 linux/arm/v7 的阶段
FROM base AS armv7

RUN apt install -y zlib1g-dev libjpeg-dev gcc curl

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

# 最终阶段，根据构建的平台选择正确的阶段
# 注意：这里的平台名称要与 buildx 的 --platform 参数一致
FROM ${TARGETPLATFORM} IN (linux/amd64, linux/arm64) ? amd64_arm64 : armv7

# 安装通用的 Python 依赖
RUN pip install --no-cache-dir flask gunicorn requests Pillow flask-cors tiktoken

# 在容器启动时运行 Flask 应用
CMD ["/app/start.sh"]
