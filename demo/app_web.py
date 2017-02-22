import os
import asyncio
import uvloop
import multiprocessing as mp
import toml
import logging
import logging.config

import noir.app as np

logging.config.dictConfig(toml.load(open('logging.toml')))

server_port = os.getenv('SERVER_PORT', 8080)
process_num = int(os.getenv('PROCESS_NUM', mp.cpu_count()))
services = os.getenv('SERVICES', '')

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def app_main():
    np.NoirApp().addCluster(
        np.create_http_server,
        np.ServerConfig(port=server_port).add_service(
            'service.test'
        ), process_num).run()

if __name__ == '__main__':
    app_main()
