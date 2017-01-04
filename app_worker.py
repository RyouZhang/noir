import time
import asyncio
import functools
import json

import router
import service

from util.rabbitmq import AsyncConsumer
import util.rabbitmq.asyncio_connection

import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def on_message_callback_finish(consumer, timer, tag, task):
    if timer is not None:
        timer.cancel()
    (res, err) = task.result()
    print(res, err)
    consumer.acknowledge_message(tag)

def on_message_callback(consumer, delivery_tag, body):
    try:
        message = json.loads(body.decode('UTF-8'))
        api = message.get('api', None)
        if api is None:
            consumer.acknowledge_message(delivery_tag)
        else:
            args = json.loads(message.get('args', '{}'))
            context = message.get('context', dict())
            context['source'] = 'ampq'

            task = asyncio.ensure_future(router.service_router.async_call_api(api, args, context, timeout = 0))
            task.add_done_callback(functools.partial(on_message_callback_finish, consumer, None, delivery_tag))
    except Exception as e:
        print('on_message_callback', e)


# AMPQ_URL,EXCHANGE_NAME,EXCHANGE_TYPE,QUEUE_NAME,ROUTING_KEY
if __name__ == '__main__':
    ampq_url = os.getenv('AMPQ_URL', None)
    assert('Invalid ampq url %s' % (ampq_url))

    exchange = os.getenv('EXCHANGE_NAME', None)
    assert('Invalid exchange name %s' % (exchange))

    exchange_type = os.getenv('EXCHANGE_TYPE', None)
    assert('Invalid exchange type %s' % (exchange_type))

    queue_name = os.getenv('QUEUE_NAME', None)
    assert('Invalid queue %s' % (queue_name))

    routing_key = os.getenv('ROUTING_KEY', '*')

    loop = asyncio.get_event_loop()
    consumer = AsyncConsumer(
        ampq_url,
        connection_class = None,
        exchange_name = exchange,
        exchange_type = exchange_type,
        queue_name = queue_name,
        routing_key = routing_key, 
        message_callback = on_message_callback,
        ioloop = loop)
    try:
        consumer.connect()
        loop.run_forever()
    except KeyboardInterrupt:
        consumer.stop()
        loop.stop()