import time
import asyncio
import functools
import threading

import pika
from pika import adapters
from pika.adapters import base_connection

import aiomysql

from util.mysql import MySQLPool
from util.rabbitmq import AsyncConsumer
import util.rabbitmq.asyncio_connection

async def test_example(loop, body):
    res = None   
    mysql_pool = await MySQLPool.get_pool('192.168.1.19', user = 'root', password = '123', db = 'stock')
    async with mysql_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT count(*) from symbols")
            (res,) = await cur.fetchone()
    return '%s|%s' % (body,res), 'good'

loop = asyncio.get_event_loop()

def on_message_callback_finish(client, t, tag, f):
    t.cancel()
    (res, msg) = f.result()
    print(res, msg, threading.current_thread())
    client.acknowledge_message(tag)

def test_timeout(h):
    print(h, threading.current_thread())
    if h.done():
        print('success')
    else:
        print('time out')

def on_message_callback(consumer, delivery_tag, body):
    t = asyncio.ensure_future(test_example(loop, body), loop = loop)
    x = loop.call_later(10, functools.partial(test_timeout, t))
    t.add_done_callback(functools.partial(on_message_callback_finish, consumer, x, delivery_tag))

def main():
    example = AsyncConsumer(
        'amqp://192.168.1.19:5672/',
        exchange_name = 'message',
        exchange_type = 'topic',
        queue_name = 'text_1',
        routing_key = 'example.text.3', 
        message_callback = on_message_callback,
        connection_class = util.rabbitmq.asyncio_connection.AsyncioConnection,
        ioloop = loop)
    try:
        example.run()
        loop.run_forever()
    except KeyboardInterrupt:
        example.stop()
        loop.stop()


if __name__ == '__main__':
    main()