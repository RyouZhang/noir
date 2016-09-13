import os
import json
import asyncio
from urllib.parse import urlparse, parse_qsl

from aiohttp import web

import router
import rule
import service
import entry

async def parser_request(request):
    args = {}
    if request.method == 'GET':
        pairs = parse_qsl(request.query_string)
    elif request.method == 'POST':
        raw = await request.content.read()
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
        User_Id = request.headers.get('HTTP_X_FIVEMILES_USER_ID', None),
        User_Token = request.headers.get('HTTP_X_FIVEMILES_USER_TOKEN', None)
    )
    return '/' + request.match_info['api'], params, context

async def handler(request):
    api, params, context = await parser_request(request)

    result, err = await rule.ruleManager.check_api_rule(api, params, context)
    if result == False and err is not None:
        return process_response(request, None, err)
    else:
        raw, err = await router.serviceRouter.async_call_api(api, params['args'], context, timeout = 5)
        return process_response(request, raw, err)

def process_response(request, raw, err):
    response = web.Response()
    if err is None:
        response.headers['HTTP_X_FIVEMILES_CODE'] = '500'
    else:
        response.headers['HTTP_X_FIVEMILES_CODE'] = '0'    
    if err is None: 
        response.body = json.dumps(raw).encode('utf-8')
    else:
        response.body = err.encode('utf-8')
    return response

if __name__ == '__main__':
    port = os.getenv('SERVER_PORT', '8080')

    app = web.Application()
    app.router.add_route('*', '/{api:.+}', handler)
    web.run_app(app)