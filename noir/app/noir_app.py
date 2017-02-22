import os
import logging
import multiprocessing as mp
import asyncio
import uvloop
import importlib


WORKER_MONITOR_TIME = 5

logger = logging.getLogger()

class NoirApp(object):

    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._clusters = []
        self._workers = []


    def addCluster(self, creater_worker, config, count=1):
        self._clusters.append((creater_worker, config, count))
        return self


    def on_timer_callback(self):
        dead_works = []
        for (worker, config) in self._workers:
            if worker.is_alive() is False:
                logger.error('the worker %s deaded (pid:%s) %s', worker.name, worker.pid, worker.exitcode)
                dead_works.append((worker, config))

        for worker_info in dead_works:
            self._workers.remove(worker_info)
            
            (create_worker, config) = worker_info
            worker = mp.Process(target=create_worker, args=(config,))
            self._workers.append((worker, config))
            worker.start()
            logger.info('the worker %s restart (pid:%s)', worker.name, worker.pid)

        loop = asyncio.get_event_loop()
        loop.call_later(WORKER_MONITOR_TIME, self.on_timer_callback)


    def run(self):
        if len(self._clusters) == 0:
            return
        
        for (create_worker, config, count) in self._clusters:
            for i in range(count):
                worker = mp.Process(target=create_worker, args=(config,))
                self._workers.append((worker, config))
        
        for (worker, config) in self._workers:
            worker.start()

        self._loop.call_later(WORKER_MONITOR_TIME, self.on_timer_callback)
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            for (worker, config) in self._workers:
                if worker.is_alive():
                    worker.terminate() 
        finally:
            self._loop.stop()
