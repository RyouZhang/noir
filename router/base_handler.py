import time
import asyncio
from urllib.parse import urlparse

import tornado.ioloop
import tornado.web
import tornado.httpserver

import util

from filter.service_filter import serviceFilter
from router.service_router import serviceRouter

class BaseHandler(tornado.web.RequestHandler):
    async def get(self):
        api, params, context = self.parser_request()

        result, err = await serviceFilter.check_api_filter(api, params, context)
        if result == False and err is not None:
            return self.process_response(None, err)

        raw, err = await serviceRouter.async_call_api(api, params.get('args', dict()), context)
        self.process_response(raw, err)

    async def post(self):
        api, params, context = self.parser_request()

        result, err = await serviceFilter.check_api_filter(api, params, context)
        if result == False and err is not None:
            return self.process_response(None, err)

        raw, err = await serviceRouter.async_call_api(api, params.get('args', dict()), context)
        self.process_response(raw, err)

    def parser_request(self):
        uri = urlparse(self.request.uri)

        params = dict(
            args = self.get_argument('args', dict()),
            timestamp = float(self.get_argument('e', '0.0')),
            sign = self.get_argument('sign', None))
        
        context = dict(
            USER_ID = self.request.headers.get('HTTP_X_FIVEMILES_USER_ID', None),
            USER_TOKEN = self.request.headers.get('HTTP_X_FIVEMILES_USER_TOKEN', None)
        )
        return uri.path, params, context


    def process_response(self, raw, err):
        if err is None:
            self.set_header('HTTP_X_FIVEMILES_CODE', 0)
            self.write(raw)
        else:
            self.set_header('HTTP_X_FIVEMILES_CODE', 500)
            self.write(err.encode('utf-8'))



