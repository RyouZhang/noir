import time
import asyncio

import pika
from pika import adapters
from pika.adapters import base_connection

from util.rabbitmq.asyncio_connection import AsyncConnection


class AsyncPublisger(object):
    def __init__(self, 
        amqp_url,
        exchange_name = None,
        exchange_type = None,
        queue_name = None,
        routing_key = None,
        connection_class = None,
        ioloop = None, 
        message_callback = None):

        self._connection_class = connection_class
        self._connection = None
        self._channel = None
        self._acked = 0
        self._nacked = 0
        self._stopping = False
        self._url = amqp_url
        self._closing = False

        self._publich_interval = 1

        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._queue_name = queue_name
        self._routing_key = routing_key
        self._ioloop = ioloop
        self._message_callback = message_callback        

    def connect(self):
        if self._connection_class is None:
            return AsyncConnection(pika.URLParameters(self._url), self.on_connection_open, ioloop = self._ioloop)
        else:
            return self._connection_class(pika.URLParameters(self._url), self.on_connection_open)

    def on_connection_open(self, unused_connection):
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        self._acked = 0
        self._nacked = 0

        # Create a new connection
        self._connection = self.connect()

    def open_channel(self):
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self._exchange_name)

    def add_on_channel_close_callback(self):
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        if not self._closing:
            self._connection.close()

    def setup_exchange(self, exchange_name):
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       exchange_name,
                                       self._exchange_type)

    def on_exchange_declareok(self, unused_frame):
        pass
        # print('on_exchange_declareok')
        # self.setup_queue(self._queue_name)

    # def setup_queue(self, queue_name):
    #     self._channel.queue_declare(self.on_queue_declareok, queue_name)

    # def on_queue_declareok(self, method_frame):
    #     self._channel.queue_bind(self.on_bindok, self._queue_name,
    #                              self._exchange_name, self._routing_key)

    def on_bindok(self, unused_frame):
        self.start_publishing()

    def start_publishing(self):
        self.schedule_next_message()

    def schedule_next_message(self):
        if self._stopping:
            return
        self._connection.add_timeout(self._publich_interval,
                                     self.publish_message)

    def publish_message(self, message = None, routing_key = None, properties = None):
        if self._stopping:
            return
        
        if message is None:
            return
        
        if routing_key is None:
            self._channel.basic_publish(
                exchange = self._exchange_name, 
                routing_key = self._routing_key, 
                body = message)
        else:
            self._channel.basic_publish(
                exchange = self._exchange_name, 
                routing_key = routing_key, 
                body = message)            
        self.schedule_next_message()

    def close_channel(self):
        if self._channel:
            self._channel.close()

    def run(self):
        self._connection = self.connect()

    def stop(self):
        self._stopping = True
        self.close_channel()
        self.close_connection()

    def close_connection(self):
        self._closing = True
        self._connection.close()
