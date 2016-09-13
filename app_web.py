import os
import json
import asyncio
from urllib.parse import urlparse, parse_qsl

import aiohttp
import aiohttp.server
from aiohttp import MultiDict

import router
import rule
import service


class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):

    async def handle_request(self, message, payload):
        api, params, context = await self.parser_request(message, payload)

        result, err = await rule.ruleManager.check_api_rule(api, params, context)
        if result == False and err is not None:
            await self.process_response(message, None, err)
        else:
            raw, err = await router.serviceRouter.async_call_api(api, params['args'], context, timeout = 5)
            await self.process_response(message, raw, err)

    async def parser_request(self, message, payload):
        url_info = urlparse(message.path)
        path = url_info.path

        args = {}
        if message.method == 'GET':
            pairs = parse_qsl(url_info.query)
        elif message.method == 'POST':
            raw = await payload.read()
            pairs = parse_qsl(raw)
        
        for (k,v) in pairs:
            args[k] = v
        
        params = dict(
            sign = args.get('sign', None),
            e = args.get('e', 0),
        )
        if args.get('args', None) is not None:
            params['args'] = json.loads(args['args'])
        else:
            params['args'] = dict()

        context = dict(
            User_Id = message.headers.get('HTTP_X_FIVEMILES_USER_ID', None),
            User_Token = message.headers.get('HTTP_X_FIVEMILES_USER_TOKEN', None)
        )
        return path, params, context

    async def process_response(self, message, raw, err):
        response = aiohttp.Response(
            self.writer, 200, http_version = message.version
        )
        if err is None:
            response.add_header('HTTP_X_FIVEMILES_CODE', '500')
        else:
            response.add_header('HTTP_X_FIVEMILES_CODE', '0')
        response.send_headers()       
        if err is None: 
            response.write(json.dumps(raw).encode('utf-8'))
        else:
            response.write(err.encode('utf-8'))
        await response.write_eof()


if __name__ == '__main__':
    port = os.getenv('SERVER_PORT', '8080')

    loop = asyncio.get_event_loop()
    f = loop.create_server(
        lambda: HttpRequestHandler(debug=True, keep_alive=90),
        '0.0.0.0', port)
    
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass