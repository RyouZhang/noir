import time
import asyncio

import pika
from pika import adapters
from pika.adapters import base_connection

class AsyncPublisger(object):
    def __init__(self, 
        amqp_url,
        connection_class,
        ioloop,
        connection_callback = None,
        max_reconnect = 0):

        self._connection = None
        self._reconntet_num = 0
        self._max_reconnect = max_reconnect
        self._channel = None
        self._stopping = False
        self._closing = False

        self._message_queue = []

        self._url = amqp_url
        self._connection_class = connection_class
        self._ioloop = ioloop
        self._connection_callback = connection_callback

    def connect(self):
        if self._connection_class is None:
            return None
        return self._connection_class(
            parameters = pika.URLParameters(self._url),
            on_open_callback = self.on_connection_open,
            on_open_error_callback = self.on_connection_open_error)

    def on_connection_open(self, connection):
        self._connection = connection
        self._reconntet_num = 0

        self.add_on_connection_close_callback()
        self.open_channel()

    def on_connection_open_error(self, connection, error):
        connection.add_timeout(5, self.reconnect) 

    def add_on_connection_close_callback(self):
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        if self._max_reconnect != 0 and self._reconntet_num >= self._max_reconnect:
            return
        self._reconntet_num = self._reconntet_num + 1
        self.connect()

    def open_channel(self):
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self._channel = channel
        self.add_on_channel_close_callback()

        while len(self._message_queue) > 0:
            msg = self._message_queue.pop()
            self.publish_message(
                body = msg['body'],
                exchange = msg['exchange'],
                routing_key = msg['routing_key'],
                properties = msg['properties'])

    def add_on_channel_close_callback(self):
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        if not self._closing:
            self._connection.close()

    def publish_message(self, body, exchange = None, routing_key = "*", properties = None):
        if self._stopping or body is None:
            return
        try:
            self._channel.basic_publish(
                exchange = exchange, 
                routing_key = routing_key, 
                body = body)   
        except Exception as e:
            self._message_queue.append(dict(body = body, exchange = exchange, routing_key = routing_key, properties = properties))
         
    def close_channel(self):
        if self._channel:
            self._channel.close()

    def stop(self):
        if len(self._message_queue) > 0:
            return
        
        self._stopping = True
        self.close_channel()
        self.close_connection()

    def close_connection(self):
        self._closing = True
        self._connection.close()
        self._connection = None
