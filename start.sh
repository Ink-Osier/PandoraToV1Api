#!/bin/bash

# 记录当前日期和时间
NOW=$(date +"%Y-%m-%d-%H-%M")

# 启动Gunicorn
exec gunicorn -w 2 --threads 2 --bind 0.0.0.0:33333 main:app --access-logfile "./log/access-${NOW}.log" --error-logfile "./log/error-${NOW}.log"

# python3 ./main.py

