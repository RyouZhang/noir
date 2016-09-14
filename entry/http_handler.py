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
        response.add_header('Transfer-Encoding', 'chunked')

        accept_encoding = message.headers.get('accept-encoding', '').lower()
        if 'gzip' in accept_encoding:
            response.add_header('Content-Encoding', 'gzip')
            response.add_compression_filter('gzip')        
        elif 'deflate' in accept_encoding:
            response.add_header('Content-Encoding', 'deflate')
            response.add_compression_filter('deflate')
        
        response.add_chunking_filter(1024)

        output_raw = None
        if err is None:
            response.add_header('HTTP_X_FIVEMILES_CODE', '0')
            response.add_header('Content-type', 'text/json')
            output_raw = json.dumps(raw).encode('utf-8')
        else:
            response.add_header('HTTP_X_FIVEMILES_CODE', '500')
            response.add_header('Content-type', 'text/plain')
            output_raw = err.encode('utf-8')
        response.send_headers()       

        response.write(output_raw)
        await response.write_eof()
        if response.keep_alive():
            self.keep_alive(True)