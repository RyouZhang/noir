import os
import multiprocessing as mp
import asyncio
import util
import uvloop

import entry


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class WebApp:
    def __init__(self, server_port=8080, process_num=mp.cpu_count(), moniter_duraton=5, register_rule=None, register_Service=None, handler_class=entry.HttpRequestHandler):
        self._process_num = process_num
        self._server_port = server_port
        self._moniter_duraton = moniter_duraton
        self._worker_array = []

        self._register_rule = None
        self._register_service = None
        self._handler_class = handler_class
        
    def run(self):
        for i in range(self._process_num):
            worker = mp.Process(
                target=launch_web_server, 
                args=(self._server_port, self._register_rule, self._register_service, self._handler_class))
            self._worker_array.append(worker)

        for worker in self._worker_array:
            worker.start()

        loop = asyncio.get_event_loop()
        loop.call_later(self._moniter_duraton, self._on_timer_callback, self._worker_array)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            for worker in self._worker_array:
                if worker.is_alive():
                    worker.terminate() 
        finally:
            loop.stop()

    def _on_timer_callback(self):
        dead_works = []
        for worker in self._worker_array:
            if worker.is_alive() is False:
                util.logger.error('the worker %s deaded (pid:%s) %s', worker.name, worker.pid, worker.exitcode)
                dead_works.append(worker)

        for worker in dead_works:
            self._worker_array.remove(worker)

        for i in range(len(dead_works)):
            worker = mp.Process(
                target=launch_web_server, 
                args=(self._server_port, self._register_rule, self._register_service, self._handler_class))
            self._worker_array.append(worker)      
            worker.start()

            util.logger.info('the worker %s restart (pid:%s)', worker.name, worker.pid)

        loop = asyncio.get_event_loop()
        loop.call_later(self._moniter_duraton, self._on_timer_callback, self._worker_array)


def launch_web_server(port, register_rule, register_service, handler_class):
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    import router
    import rule
    import service

    if register_rule is not None:
        register_rule()
    if register_service is not None:
        register_service()

    loop = asyncio.get_event_loop()
    f = loop.create_server(lambda: handler_class(debug=False, tcp_keepalive=True, keepalive_timeout=env.consts.KEEP_ALIVE), '0.0.0.0',
                           port, reuse_port=True)
    
    srv = loop.run_until_complete(f)

    util.logger.info('server on %s', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
    loop.close()
