import time
import asyncio
import functools
import json

import router
import service

from util.rabbitmq import AsyncConsumer
import util.rabbitmq.asyncio_connection

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
            task = asyncio.ensure_future(router.serviceRouter.async_call_api(api, args, context, timeout = 10))
            task.add_done_callback(functools.partial(on_message_callback_finish, consumer, None, delivery_tag))
    except Exception as e:
        print('on_message_callback', e)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    consumer = AsyncConsumer(
        'amqp://192.168.1.19:5672/',
        connection_class = None,
        exchange_name = 'message',
        exchange_type = 'topic',
        queue_name = 'text_1',
        routing_key = 'example.text.3', 
        message_callback = on_message_callback,
        ioloop = loop)
    try:
        consumer.connect()
        loop.run_forever()
    except KeyboardInterrupt:
        consumer.stop()
        loop.stop()