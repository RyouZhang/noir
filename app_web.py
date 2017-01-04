import os
import multiprocessing as mp
import asyncio
import util
import uvloop

import environment as env

server_port = os.getenv('SERVER_PORT', env.consts.SERVER_PORT)
process_num = int(os.getenv('PROCESS_NUM', mp.cpu_count()))

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def launch_web_server(port):

    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    import router
    import rule
    import service
    import entry
    import util

    loop = asyncio.get_event_loop()
    f = loop.create_server(lambda: entry.HttpRequestHandler(debug=False, tcp_keepalive=True, keepalive_timeout=env.consts.KEEP_ALIVE), '0.0.0.0',
                           port, reuse_port=True)
    
    srv = loop.run_until_complete(f)

    util.logger.info('server on %s', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
    loop.close()


def create_worker(port):
    return mp.Process(target=launch_web_server, args=(port,))


def on_timer_callback(workers):
    dead_works = []
    for worker in workers:
        if worker.is_alive() is False:
            util.logger.error('the worker %s deaded (pid:%s) %s', worker.name, worker.pid, worker.exitcode)
            dead_works.append(worker)

    for worker in dead_works:
        workers.remove(worker)

    for i in range(len(dead_works)):
        worker = create_worker(server_port)
        workers.append(worker)      
        worker.start()
        util.logger.info('the worker %s restart (pid:%s)', worker.name, worker.pid)

    loop = asyncio.get_event_loop()
    loop.call_later(env.consts.WORKER_MONITOR_TIME, on_timer_callback, workers)


def app_main():

    workers = []
    for i in range(process_num):
        workers.append(create_worker(server_port))

    for worker in workers:
        worker.start()

    loop = asyncio.get_event_loop()
    loop.call_later(env.consts.WORKER_MONITOR_TIME, on_timer_callback, workers)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        for worker in workers:
            if worker.is_alive():
                worker.terminate() 
    finally:
        loop.stop()


if __name__ == '__main__':
    util.logger.info("SERVER_PORT=%s" % server_port)
    util.logger.info("PROCESS_NUM=%s" % process_num)
    app_main()
