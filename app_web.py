import os
import multiprocessing as mp
import asyncio
import util
import uvloop

import app

server_port = os.getenv('SERVER_PORT', 8080)
process_num = int(os.getenv('PROCESS_NUM', mp.cpu_count()))

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def app_main():
    config = app.ServerConfig().set_port(server_port)
    app.run_web_server(config, process_num=process_num)

if __name__ == '__main__':
    app_main()
