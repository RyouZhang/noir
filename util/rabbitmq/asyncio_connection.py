import time
import asyncio

import pika
from pika import adapters
from pika.adapters import base_connection


class AsyncConnection(base_connection.BaseConnection):

    def __init__(self,
                 parameters = None,
                 on_open_callback = None,
                 on_open_error_callback = None,
                 on_close_callback = None,
                 stop_ioloop_on_close = False,
                 ioloop = None):
        
        self.sleep_counter = 0
        if ioloop is None:
            self.ioloop = asyncio.get_event_loop()
        else:
            self.ioloop = ioloop

        super(AsyncConnection, self).__init__(
            parameters,
            on_open_callback,
            on_open_error_callback,
            on_close_callback,
            self.ioloop,
            stop_ioloop_on_close)
    
    def _adapter_connect(self):
        err = super(AsyncConnection, self)._adapter_connect()
        if not err:
            self.ioloop.add_reader(self.socket.fileno(), self.read_data)
            self.ioloop.add_writer(self.socket.fileno(), self.write_data)
        return err
    
    def read_data(self):
        super(AsyncConnection, self)._handle_events(self.socket.fileno(), self.event_state, None, False)
    
    def write_data(self):
        super(AsyncConnection, self)._handle_events(self.socket.fileno(), self.event_state, None, False)

    def _adapter_disconnect(self):
        if self.socket:
            self.ioloop.remove_reader(self.socket.fileno())
            self.ioloop.remove_writer(self.socket.fileno())
        super(AsyncConnection, self)._adapter_disconnect()
    
    def add_timeout(self, deadline, callback_method):
        return self.ioloop.call_later(deadline, callback_method)
    
    def remove_timeout(self, timeout_handle):
        timeout_handle.cancel()