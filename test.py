import pymysql
import asyncio
from aiomysql import create_pool
import pymysql.cursors

# import csv


# def load_nasdaq_stock_symbol_info(file_path, exchange):
#     stock_symbols = []
#     with open(file_path, newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#         row_index = 0

#         for row in spamreader:
#             if row_index == 0:
#                 row_index = row_index + 1
#                 continue
#             row_index = row_index + 1
            
#             symbol = row[0].strip()
#             stock_symbols.append({
#                 "symbol": symbol,
#                 "name": row[1],
#                 "sector": row[5],
#                 "industry": row[6],
#                 "exchange": exchange
#             })
#     return stock_symbols


# stock_symbols = load_nasdaq_stock_symbol_info('./nasdaq.csv', 'NSADAQ')

# conn = pymysql.connect(
#         host = '192.168.1.19',
#         user = 'root',
#         password = '123',
#         db = 'stock',
#         charset = 'utf8')
# with conn.cursor() as cr:
#     for stock_symbol in stock_symbols:
#         cr.execute('insert into symbols(name, code, industry, sector) values(%s, %s, %s, %s)', 
#             (stock_symbol['name'], stock_symbol['symbol'], stock_symbol['industry'], stock_symbol['sector']))
# conn.commit()

# with conn.cursor() as cr:
#     cr.execute('select count(*) from symbols')
#     res = cr.fetchone()
#     print(res)
# conn.close()


async def test_example(loop):
    async with create_pool(
        host = '192.168.1.19', 
        port = 3306, 
        user = 'root', 
        password = '123', 
        db = 'stock', 
        loop = loop) as pool:

        async with pool.acquire() as conn:
            async with conn.cursor() as cr:
                await cr.execute('select * from symbols where code = %s', ('AAPL',))
                res = await cr.fetchone()
                print(res)

loop = asyncio.get_event_loop()
loop.run_until_complete(test_example(loop))