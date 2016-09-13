import os
import asyncio
from aiohttp import web

import router
import rule
import service
import entry


async def handler(request):
    return web.Response(body = b'hello world')
#     api, params, context = await parser_request(request)

#     result, err = await rule.ruleManager.check_api_rule(api, params, context)
#     if result == False and err is not None:
#         await self.process_response(message, None, err)
#     else:
#         raw, err = await router.serviceRouter.async_call_api(api, params['args'], context, timeout = 5)
#         await self.process_response(message, raw, err)
#     return web.Response()

# async def parser_request(request):
#     url_info = urlparse(message.path)
#     path = request.path

#     args = {}
#     if message.method == 'GET':
#         pairs = parse_qsl(url_info.query)
#     elif message.method == 'POST':
#         raw = await payload.read()
#         pairs = parse_qsl(raw)
    
#     for (k,v) in pairs:
#         args[k] = v
    
#     params = dict(
#         sign = args.get('sign', None),
#         e = args.get('e', 0),
#     )
#     if args.get('args', None) is not None:
#         params['args'] = json.loads(args['args'])
#     else:
#         params['args'] = dict()

#     context = dict(
#         User_Id = message.headers.get('HTTP_X_FIVEMILES_USER_ID', None),
#         User_Token = message.headers.get('HTTP_X_FIVEMILES_USER_TOKEN', None)
#     )
#     return path, params, context

# async def process_response(self, message, raw, err):
#     response = aiohttp.Response(
#         self.writer, 200, http_version = message.version
#     )
#     if err is None:
#         response.add_header('HTTP_X_FIVEMILES_CODE', '500')
#     else:
#         response.add_header('HTTP_X_FIVEMILES_CODE', '0')
#     response.send_headers()       
#     if err is None: 
#         response.write(json.dumps(raw).encode('utf-8'))
#     else:
#         response.write(err.encode('utf-8'))
#     await response.write_eof()

if __name__ == '__main__':
    port = os.getenv('SERVER_PORT', '8080')

    app = web.Application()
    app.router.add_route('*', '/', handler)
    web.run_app(app)