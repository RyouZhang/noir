import asyncio
import functools

import pika.adapters
from util.rabbitmq.async_publisher import AsyncPublisger

# AMPQ_URL
class RabbitMQPool():
    def __init__(self):
        self._lockDic = dict() 
        self._clientDic = dict()
    
    async def get_publisher(self, url, connection_class = None):
        key = '%s' % (url)
        client = self._clientDic.get(key, None)
        if client is not None:
            return client
        try:
            lock = self._lockDic.get(key, asyncio.Lock())
            self._lockDic[key] = lock
            await lock.acquire()

            client = self._clientDic.get(key, None)
            if client is None:
                client = AsyncPublisger(
                    url,
                    ioloop = asyncio.get_event_loop(),
                    connection_class = pika.adapters.TornadoConnection)
            client.connect()
            self._clientDic[key] = client
        finally:
            lock = self._lockDic[key]
            lock.release()
            del self._lockDic[key]
        return client

rabbitMQPool = RabbitMQPool()