# Fmsh_Search
A python web service sample base on aiohttp, for python 3.5+

## Dependent
- uvloop
- aiohttp
- aioredis
- aiomysql
- pika
- toml

## 环境的搭建
建议使用dockerfile来快速构成测试环境

docker build ~/YOUR_CODE_DIR

## Docker运行方式
docker run -it -v ~/YOUR_CODE_DIR:/code -p 8080:8080 YOUR_REP_NAME:REP_TAG /bin/bash
