import time
import asyncio
import aiohttp
import aiohttp.server
from urllib.parse import urlparse, parse_qsl

from router.service_router import service_router
import util


class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):
    async def handle_request(self, message, payload):
        start_time = util.get_timestamp()
        api, args, context = await self.parse_request_handler(message, payload)
        raw, err = await service_router.async_call_api(api, args, context, 10)
        util.logger.info('%s|%s|%s|%s', api, args, context, util.get_timestamp() - start_time)
        await self._process_response(message, raw, err)


    async def parse_request_handler(self, message, payload):
        url_info = urlparse(message.path)
        path = url_info.path

        args = {}
        if message.method == 'GET':
            args = {k:v for (k, v)in parse_qsl(url_info.query)}
        elif message.method == 'POST':
            raw = await payload.read()
            args = {k:v for (k, v)in parse_qsl(raw)}

        return path, args, dict()


    def prepare_response_handler(self, message, raw, err):
        if err is not None:
            response = aiohttp.Response(
                self.writer, 500, http_version = message.version, close = message.should_close
            )   
            return response, err.encode('utf-8')

        response = aiohttp.Response(
            self.writer, 200, http_version = message.version, close = message.should_close
        )   
        return response, raw.encode('utf-8')


    async def _process_response(self, message, raw, err):
        try:
            response, raw = self.prepare_response_handler(message, raw, err)
            response.add_header('Transfer-Encoding', 'chunked')

            accept_encoding = message.headers.get('accept-encoding', '').lower()
            if 'gzip' in accept_encoding:
                response.add_header('Content-Encoding', 'gzip')
                response.add_compression_filter('gzip')
                response.add_chunking_filter(8192)
            elif 'deflate' in accept_encoding:
                response.add_header('Content-Encoding', 'deflate')
                response.add_compression_filter('deflate')
                response.add_chunking_filter(8192)

            response.send_headers()
            if raw is not None:
                response.write(raw)

            await response.write_eof()
            if response.keep_alive():
                self.keep_alive(True)

        except Exception as e:
            self.keep_alive(False)
