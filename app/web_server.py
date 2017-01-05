import os
import multiprocessing as mp
import asyncio
import util
import uvloop

import entry
import importlib
import importlib.util

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

WORKER_MONITOR_TIME = 5

class ServerConfig:

    def __init__(self, port=80):
        self.port = port
        self.keep_alive = True
        self.keep_alive_timeout = 90
        self.handler_class = entry.HttpRequestHandler
        self.services = []

    def set_keep_alive(self, flag, timeout=90):
        self.keep_alive = flag
        self.keep_alive_timeout = timeout
        return self


    def add_service(self, service_module):
        if type(service_module) is list:
            self.services = self.services + service_module
        elif type(service_module) is str and len(service_module) > 0:
            self.services.append(service_module)
        return self 
    
    def set_handler_class(self, handler_class):
        self.handler_class = handler_class
        return self


workers = []

def run_web_server(config, process_num=mp.cpu_count()):
    for i in range(process_num):
        workers.append(create_worker(config))

    for worker in workers:
        worker.start()

    loop = asyncio.get_event_loop()
    loop.call_later(WORKER_MONITOR_TIME, on_timer_callback, config)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        for worker in workers:
            if worker.is_alive():
                worker.terminate() 
    finally:
        loop.stop()


def launch_server(config):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    import router

    for service_name in config.services:
        importlib.import_module(service_name)

    loop = asyncio.get_event_loop()
    f = loop.create_server(
        lambda: entry.HttpRequestHandler(
            debug=True,
            tcp_keepalive=config.keep_alive,
            keepalive_timeout=config.keep_alive_timeout),
        '0.0.0.0', config.port, reuse_port=True)

    srv = loop.run_until_complete(f)

    util.logger.info('server on %s', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
    loop.close()


def create_worker(config):
    return mp.Process(target=launch_server, args=(config,))


def on_timer_callback(config):
    dead_works = []
    for worker in workers:
        if worker.is_alive() is False:
            util.logger.error('the worker %s deaded (pid:%s) %s', worker.name, worker.pid, worker.exitcode)
            dead_works.append(worker)

    for worker in dead_works:
        workers.remove(worker)

    for i in range(len(dead_works)):
        worker = create_worker(config)
        workers.append(worker)      
        worker.start()
        util.logger.info('the worker %s restart (pid:%s)', worker.name, worker.pid)

    loop = asyncio.get_event_loop()
    loop.call_later(WORKER_MONITOR_TIME, on_timer_callback, config)
