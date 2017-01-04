import asyncio
import aioredis

# REDIS_HOST, REDIS_PORT, REDIS_PWD
class RedisDBPool():
    def __init__(self):
        self._lock = asyncio.Lock()
        self._poolDic = dict()
    
    async def get_pool(self, host, port = 6379, password = None):
        key = 'redis://%s:%d' % (host, port)

        pool = self._poolDic.get(key, None)
        if pool is not None:
            return pool
        
        try:
            await self._lock.acquire()
            pool = self._poolDic.get(key, None)
            if pool is None:
                pool = await aioredis.create_pool(
                    (host, port),
                    password = password,
                    minsize = 4,
                    maxsize = 16)
                self._poolDic[key] = pool
        finally:
            self._lock.release()
        return pool

RedisPool = RedisDBPool()