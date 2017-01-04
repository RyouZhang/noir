FROM python:latest
MAINTAINER ryou
LABEL version="nori"
RUN apt-get update && apt-get install -y wget
RUN pip install --upgrade pip
RUN pip install aioredis aiomysql aiohttp uvloop pika toml