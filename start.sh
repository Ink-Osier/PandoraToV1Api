#!/bin/bash

# 记录当前日期和时间
NOW=$(date +"%Y-%m-%d-%H-%M")

# 启动 Gunicorn 并使用 tee 命令同时输出日志到文件和控制台
exec gunicorn -w 2 --threads 2 --bind 0.0.0.0:33333 main:app --access-logfile - --error-logfile - | tee "./log/access-${NOW}.log"

# python3 ./main.py

