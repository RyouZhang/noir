import aiohttp

import router
import util.http

class HttpProxyV1(router.ApiHandler):
    async def process(self, args, context):
        resp, err = await util.http.async_http('GET', 'https://www.google.com')
        if err is not None:
            return None, err
        elif resp.status == 200:
            raw = await resp.read()
            return raw.decode('utf-8'), None
        else:
            return None, resp.reason


router.register_api_handler('/api/http/proxy/v1', HttpProxyV1())