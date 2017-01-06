FROM python:latest
MAINTAINER ryou
LABEL version="noir"
RUN apt-get update && apt-get install -y wget
RUN pip install --upgrade pip
RUN pip install aiohttp uvloop
RUN pip install git+https://github.com/RyouZhang/noir.git@master