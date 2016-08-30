import time
import asyncio
from urllib.parse import urlparse

import tornado.ioloop
import tornado.web
import tornado.httpserver

import util
import filter
from router.api_handler import ApiHandler

api_router_dic = dict()

def register_api(api, handler):
    api = '/api/' + api
    temp = api_router_dic.get(api, None)
    assert(temp is None), 'dupilicate api %s: %s, %s' % (api, temp, handler)
    api_router_dic[api] = handler

def find_api_handler(api):
    print(api)
    handler = api_router_dic.get(api, None)
    if handler is None:
        return None, 'Invalid API {}'.format(api)
    return handler, None


class BaseHandler(tornado.web.RequestHandler):
    async def get(self):
        api, params, context = self.parser_request()

        raw, err = await self.exec_api_handler(api, params, context)

        self.process_response(raw, err)


    async def post(self):
        api, params, context = self.parser_request()

        raw, err = await self.exec_api_handler(api, params, context)

        self.process_response(raw, err)


    async def exec_api_handler(self, api, params, context):
        handler, err = find_api_handler(api)
        if err is not None:
            return None, err    
        
        for func in handler.filters:
            res, err = func(params.get('timestamp', None), params.get('sign', None), params.get('args', dict()), context)
            if res == False:
                return None, err           
        try:
            raw, err = handler.process(params.get('args', dict()), context)
            return raw, err
        except Exception as e:
            print('call_api_error %s:%s,%s,%s' % (e, api, params, context))
            return None, 'Internal_Error'


    def parser_request(self):
        print(self.request.uri)
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



