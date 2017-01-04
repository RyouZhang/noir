import time
import asyncio
import aiohttp
import aiohttp.server

import router
import service
import util


#async def parse_request_handler(message, payload) -> api, args, context
#def prepare_response_handler(response, raw, err) -> reponse, raw

class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):
    def __init__(self, parse_request_handler, prepare_response_handler, timeout=10):
        self._parse_request_handler = parse_request_handler
        self._prepare_response_handler = prepare_response_handler
        self._timeout = timeout


    async def handle_request(self, message, payload):
        start_time = util.get_timestamp()

        if self._parse_request_handler is None:
            await self.process_response(message, None, 'Invalid_Parse_Request')
        else:
            api, params, context = await self._parse_request_handler(message, payload)
            raw, err = await router.service_router.async_call_api(api, params, context, self._timeout)
            util.logger.info('%s|%s|%s|%s', api, params, context, util.get_timestamp() - start_time)
            await self.process_response(message, raw, err)


    async def process_response(self, message, raw, err):
        try:
            status = 200
            response = aiohttp.Response(
                self.writer, status, http_version = message.version, close = message.should_close
            )
            response.add_header('Transfer-Encoding', 'chunked')

            if self._prepare_response_handler is not None:
                response, raw= self._prepare_response_handler(response, raw, err)

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

                response.send_headers()
                response.write(json.dumps(raw).encode('utf-8'))
            else:
                if raw is not None:
                    response.write(raw)
                response.send_headers()

            await response.write_eof()
            if response.keep_alive():
                self.keep_alive(True)

        except Exception as e:
            self.keep_alive(False)
