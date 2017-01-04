import time
import asyncio

import pika
from pika import adapters
from pika.adapters import base_connection
from util.rabbitmq.asyncio_connection import AsyncioConnection


class AsyncConsumer(object):

    def __init__(self, 
        ampq_url, 
        connection_class,
        ioloop,
        exchange_name = None,
        exchange_type = None,
        queue_name = None,
        routing_key = None,
        message_callback = None):
        
        self._connection = None,
        self._channel = None
        self._closing = False
        self._consumer_tag = None

        self._url = ampq_url
        # self._ioloop = ioloop
        self._connection_class = connection_class

        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._queue_name = queue_name
        self._routing_key = routing_key

        self._message_callback = message_callback
    
    def connect(self):
        if self._connection_class is None:
            self._connection_class = AsyncioConnection
        return self._connection_class(
            parameters = pika.URLParameters(self._url), 
            on_open_callback = self.on_connection_open, 
            on_open_error_callback = self.on_connection_open_error,
            ioloop = self._ioloop)

    def close_connect(self):
        self._connection.close()
    
    def add_on_connection_close_callback(self):
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        connection.add_timeout(5, self.reconnect)
        self._connection = None

    def on_connection_open(self, connection):
        self._connection = connection
        self.add_on_connection_close_callback()
        self.open_channel()

    def on_connection_open_error(self, connection, error):
        connection.add_timeout(5, self.reconnect)
    
    def reconnect(self):
        if not self._closing:
            self._connection = self.connect()

    def add_on_channel_close_callback(self):
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        self._connection.close()

    def on_channel_open(self, channel):
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self._exchange_name)

    def setup_exchange(self, exchange_name):
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       exchange_name,
                                       self._exchange_type)

    def on_exchange_declareok(self, unused_frame):
        self.setup_queue(self._queue_name)

    def setup_queue(self, queue_name):
        self._channel.queue_declare(self.on_queue_declareok, queue_name)

    def on_queue_declareok(self, method_frame):
        self._channel.queue_bind(self.on_bindok, self._queue_name,
                                 self._exchange_name, self._routing_key)

    def add_on_cancel_callback(self):
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        if self._channel:
            self._channel.close()

    def acknowledge_message(self, delivery_tag):
        self._channel.basic_ack(delivery_tag)

    def on_message(self, unused_channel, basic_deliver, properties, body):        
        if self._message_callback is None:
            self.acknowledge_message(basic_deliver.delivery_tag)
        else:
            self._message_callback(self, basic_deliver.delivery_tag, body)

    def on_cancelok(self, unused_frame):
        self.close_channel()

    def stop_consuming(self):
        if self._channel:
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def start_consuming(self):
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self._queue_name)

    def on_bindok(self, unused_frame):
        self.start_consuming()

    def close_channel(self):
        self._channel.close()

    def open_channel(self):
        self._connection.channel(on_open_callback = self.on_channel_open)

    def stop(self):
        self._closing = True
        self.stop_consuming()

