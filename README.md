# Fmsh_Search
A python web service sample base on aiohttp, for python 3.5+

## Dependent
- uvloop
- aiohttp
- aioredis
- aiomysql
- pika

## 环境的搭建
建议使用dockerfile来快速构成测试环境

docker build ~/YOUR_CODE_DIR

## Docker运行方式
docker run -it -v ~/YOUR_CODE_DIR:/code -p 8080:8080 YOUR_REP_NAME:REP_TAG /bin/bash

## Enviroment变量
- VER_TAG (源代码的tag)

- SERVER_PORT (default: 8080)
- PROCESS_NUM (default: cpu_count)
- REDIS_HOST
- REDIS_PORT
- REDIS_PWD
- MYSQL_HOST
- MYSQL_PORT
- MYSQL_USER
- MYSQL_PWD
- AMPQ_URL

## News环境变量
- ES_NEWS_HOST


## 错误处理机制, 文本翻译
## url 参数，返回值，错误码, 版本号

## 日志输出，采集，同步

## 内部服务的http请求日志监控：执行时间，请求参数，返回数据

## 自动化部署：本地开发与测试，代码提交，各环境的自动部署
