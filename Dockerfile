FROM python:latest
MAINTAINER ryou
LABEL version="nori v0.0.1"
RUN apt-get update && apt-get install -y wget
RUN pip install --upgrade pip
RUN pip install aiohttp uvloop