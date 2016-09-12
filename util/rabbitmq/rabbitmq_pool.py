import asyncio

import pika.adapters
from util.rabbitmq.asyncio_publisher import AsyncPublisger

# AMPQ_URL
class RabbitMQPool():
    def __init__(self):
        self._lock = asyncio.Lock()
        self._poolDic = dict()
    
    async def get_pool(self, amqp_url, exchange_name, exchange_type):
        if exchange_name is None:
            return None

        key = '%s:%s' % (amqp_url, exchange_name)
        pool = self._poolDic.get(key, None)
        if pool is None:
            try:
                await self._lock.acquire()
                pool = AsyncPublisger(
                    amqp_url,
                    exchange_name = exchange_name,
                    exchange_type = exchange_type,
                    connection_class = pika.adapters.TornadoConnection)
                pool.run()
                self._poolDic[key] = pool
            finally:
                self._lock.release()
        return pool

rabbitMQPool = RabbitMQPool()