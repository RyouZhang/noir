import time
import json

import router
import asyncio
import pymysql
import aiomysql

from util.mysql import MySQLPool
from util.redis import RedisPool

class StockInfoV1(router.ApiHandler):
    async def process(self, args, context):
        symbol_code = args.get('symbol', None)
        if symbol_code is None:
            return None, 'No_Symbol'
        
        stock = None
        try:
            redis_pool = await RedisPool.get_pool('192.168.1.19', 6379, db = 0)
            async with redis_pool.get() as redis:
                res = await redis.get(symbol_code)
                if res:
                    try:
                        stock = json.loads(res.decode('utf-8'))
                        await redis.expire(symbol_code, 300)
                        return stock, None
                    except Exception as e:
                        await redis.delete(symbol_code)
                
            mysql_pool = await MySQLPool.get_pool('192.168.1.19', user = 'root', password = '123', db = 'stock')
            async with mysql_pool.acquire() as mysql:
                async with mysql.cursor(cursor = aiomysql.cursors.DictCursor) as cr:
                    await cr.execute('select id, name, code, industry, sector from symbols where code in %s', ([symbol_code],))
                    stock = await cr.fetchone()
                    if stock is None:
                        return None, 'Invalid_Symbol'

            async with redis_pool.get() as redis:
                try:
                    raw = json.dumps(stock)
                    await redis.set(symbol_code, raw)
                    await redis.expire(symbol_code, 300)            
                except Exception as e:
                    pass  
                                      
            return stock, None
        except Exception as e:
            return None, str(e)

router.register_api_handler('/api/stock/info/v1', StockInfoV1())