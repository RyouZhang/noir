import asyncio
import pymysql
import aiomysql

# MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PWD, MYSQL_DB
class MySqlDBPool():
    def __init__(self):
        self._lock = asyncio.Lock()
        self._poolDic = dict()
    
    async def get_pool(self, host, port = 3306, user = 'root', password = '', db = 'mysql'):
        key = 'mysql://%s:%s@%s:%d/%s' % (user, password, host, port, db)
        
        pool = self._poolDic.get(key, None)
        if pool is not None:
            return pool 
        
        try:
            await self._lock.acquire()
            pool = self._poolDic.get(key, None)
            if pool is None:
                pool = await aiomysql.create_pool(
                        host = host,
                        port = port,
                        user = user,
                        password = password,
                        db = db,
                        minsize = 4,
                        maxsize = 16,
                        connect_timeout = 5,
                        loop = asyncio.get_event_loop())
                self._poolDic[key] = pool
        finally:
            self._lock.release()
        return pool

MySQLPool = MySqlDBPool()