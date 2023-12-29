#!/bin/bash

# 记录当前日期和时间
NOW=$(date +"%Y-%m-%d-%H-%M")

# 尝试从环境变量获取参数，如果不存在，则从 config.json 文件中读取
# 如果这些值仍然不存在，将它们设置为默认值

if [ -z "$PROCESS_WORKERS" ]; then
    PROCESS_WORKERS=$(jq -r '.process_workers // empty' /app/data/config.json)
    export PROCESS_WORKERS

    if [ -z "$PROCESS_WORKERS" ]; then
        PROCESS_WORKERS=1
    fi
fi

if [ -z "$PROCESS_THREADS" ]; then
    PROCESS_THREADS=$(jq -r '.process_threads // empty' /app/data/config.json)
    export PROCESS_THREADS

    if [ -z "$PROCESS_THREADS" ]; then
        PROCESS_THREADS=2
    fi
fi

export PROCESS_WORKERS
export PROCESS_THREADS

echo "PROCESS_WORKERS: ${PROCESS_WORKERS}"
echo "PROCESS_THREADS: ${PROCESS_THREADS}"

# 启动 Gunicorn 并使用 tee 命令同时输出日志到文件和控制台
exec gunicorn -w ${PROCESS_WORKERS} --threads ${PROCESS_THREADS} --bind 0.0.0.0:33333 main:app --access-logfile - --error-logfile -
