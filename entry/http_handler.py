import base64
import time
import json
import asyncio
from urllib.parse import urlparse, parse_qsl

import aiohttp
import aiohttp.server
from aiohttp import MultiDict

import router
import service
import util


class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):

    async def handle_request(self, message, payload):
        start_time = util.get_timestamp()
        api, params, context = await self.parser_request(message, payload)
        raw, err = await router.service_router.async_call_api(api, params, context, timeout=5)
        util.logger.info('%s|%s|%s|%s', api, params, context, util.get_timestamp() - start_time)
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
        
        for (k, v) in pairs:
            args[k] = v
        
        context = dict(
            sign=args.get('sign', None),
            timestamp=args.get('e', 0),
            user_id=message.headers.get('X_FIVEMILES_USER_ID', None),
            user_token=message.headers.get('X_FIVEMILES_USER_TOKEN', None)
        )
        params = json.loads(args.get('args', '{}'))
        
        return path, params, context

    async def process_response(self, message, raw, err):
        try:
            status = 200
            response = aiohttp.Response(
                self.writer, status, http_version = message.version, close = message.should_close
            )
            response.add_header('Transfer-Encoding', 'chunked')

            if err is None:
                accept_encoding = message.headers.get('accept-encoding', '').lower()
                if 'gzip' in accept_encoding:
                    response.add_header('Content-Encoding', 'gzip')
                    response.add_compression_filter('gzip')
                    response.add_chunking_filter(8192)
                elif 'deflate' in accept_encoding:
                    response.add_header('Content-Encoding', 'deflate')
                    response.add_compression_filter('deflate')
                    response.add_chunking_filter(8192)

                response.add_header('X_FIVEMILES_CODE', '0')
                response.add_header('Content-type', 'application/json')
                response.send_headers()

                response.write(json.dumps(raw).encode('utf-8'))
            else:
                response.add_header('X_FIVEMILES_CODE', '500')
                response.add_header('X_FIVEMILES_MSG', base64.b64encode(err.encode('utf-8')).decode('utf-8'))
                response.add_header('Content-type', 'text/plain')
                response.send_headers()

            await response.write_eof()
            if response.keep_alive():
                self.keep_alive(True)

        except Exception as e:
            self.keep_alive(False)
