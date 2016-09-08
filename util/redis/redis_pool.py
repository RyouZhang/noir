import asyncio
import aioredis

class RedisDBPool():
    def __init__(self):
        self._lock = asyncio.Lock()
        self._poolDic = dict()
    
    async def get_pool(self, host, port = 6379, db = 0, password = None):
        key = 'redis://%s:%d/%d' % (host, port, db)

        pool = self._poolDic.get(key, None)
        if pool is None:
            try:
                await self._lock.acquire()
                pool = await aioredis.create_pool(
                    (host, port),
                    db = db,
                    password = password,
                    minsize = 4,
                    maxsize = 16,
                    loop = asyncio.get_event_loop())
                self._poolDic[key] = pool
            finally:
                self._lock.release()
        return pool

RedisPool = RedisDBPool()