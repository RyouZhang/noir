import asyncio

import pika.adapters
from util.rabbitmq.asyncio_publisher import AsyncPublisger

# AMPQ_URL
class RabbitMQPool():
    def __init__(self):
        self._lockDic = dict()
        self._clientDic = dict()
    
    def connection_callback(self, client):
        self._clientDic[client._url] = client
        # 
    
    async def get_pool(self, amqp_url):
        if exchange_name is None:
            return None

        key = '%s' % (amqp_url)
        client = self._clientDic.get(key, None)
        if pool is None:
            try:
                lock = self._lockDic.get(key, asyncio.Lock())
                self._lockDic[key] = lock
                await lock.acquire()
                
                client = AsyncPublisger(
                    amqp_url,
                    connection_class = pika.adapters.TornadoConnectio,
                    connection_callback = connection_callback)
                client.run()
            finally:
                lock.release()
                self._lockDic
        return pool

rabbitMQPool = RabbitMQPool()