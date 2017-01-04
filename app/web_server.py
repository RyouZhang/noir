import os
import multiprocessing as mp
import asyncio
import util
import uvloop

import entry
import importlib

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

WORKER_MONITOR_TIME = 5

__all__ = [
    'ServerConfig',
    'run_web_server'
]


class ServerConfig:

    def __init__(self):
        self.port = 80
        self.keep_alive = True
        self.keep_alive_timeout = 90
        self.handler_class = entry.HttpRequestHandler
        self.services = []

    def set_port(self, port):
        self.port = port
        return self

    def set_keep_alive(self, flag):
        self.keep_alive = flag
        return self

    def set_keep_alive_timeout(self, flag):
        self.keep_alive_timeout = flag
        return

    def add_service(self, service_module):
        if service_module is type(list):
            self.services = self.services + service_module
        else:
            self.services.append(service_module)
        return self 
    
    def set_handler_class(self, handler_class):
        self.handler_class = handler_class
        return self


def run_web_server(config, process_num=mp.cpu_count()):
    workers = []
    for i in range(process_num):
        workers.append(create_worker(config))

    for worker in workers:
        worker.start()

    loop = asyncio.get_event_loop()
    loop.call_later(WORKER_MONITOR_TIME, on_timer_callback, (workers,config,))
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
    import service

    for service_name in config.services:
        importlib.import_module(service_name)

    loop = asyncio.get_event_loop()
    server = loop.create_server(
        lambda: config.handler_class(
            debug=False,
            tcp_keepalive=config.keep_alive,
            keepalive_timeout=config.keep_alive_timeout),
        '0.0.0.0', config.port, reuse_port=True)

    srv = loop.run_until_complete(server)

    util.logger.info('server on %s', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
    loop.close()


def create_worker(config):
    return mp.Process(target=launch_server, args=(config))


def on_timer_callback(workers, config):
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
    loop.call_later(WORKER_MONITOR_TIME, on_timer_callback, (workers, config))
