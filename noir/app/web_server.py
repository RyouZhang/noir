import os
import logging
import multiprocessing as mp
import asyncio
import uvloop
import importlib
import functools
from urllib.parse import urlparse, parse_qsl

from aiohttp import web
import noir.util as util

logger = logging.getLogger()

class ServerConfig:

    def __init__(self, port=80, parse_request=None, prepare_response=None):
        self.port = port
        self.keep_alive = True
        self.keep_alive_timeout = 90
        self.services = []
        self.parse_request = parse_request
        self.prepare_response = prepare_response


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
    

async def default_parse_request(request):
    path = request.path
    args = {}
    if request.method == 'GET':
        args = {k:v for (k, v)in parse_qsl(request.query_string)}
    elif request.method == 'POST':
        raw = await request.read()
        args = {k:v for (k, v)in parse_qsl(raw)}
    return path, args, dict()


async def default_prepare_response(raw, err):
    if err is None:
        return web.Response(status=200, body=raw.encode('utf-8'))
    else:
        return web.Response(status=500, body=err.encode('utf-8'))


async def server_handler(config, request):
   

    (parse_request, prepare_response) = config
    start_time = util.get_timestamp()
    api, args, context = await parse_request(request)
    raw, err = await service_router.async_call_api(api, args, context, 10)
    logger.info('%s|%s|%s|%s', api, args, context, util.get_timestamp() - start_time)
    return await prepare_response(raw, err)


def create_http_server(config):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    import noir.router
    from noir.router.service_router import service_router

    for service_name in config.services:
        importlib.import_module(service_name)

    srv = web.Server(
        functools.partial(server_handler, 
        (config.parse_request or default_parse_request, config.prepare_response or default_prepare_response)),
        tcp_keepalive=config.keep_alive,
        keepalive_timeout=config.keep_alive_timeout)

    loop = asyncio.get_event_loop()

    f = asyncio.get_event_loop().create_server(srv, '0.0.0.0', config.port, reuse_port=True)
    t = loop.run_until_complete(f)

    logger.info('server on %s', t.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(srv.shutdown())
    loop.close()
