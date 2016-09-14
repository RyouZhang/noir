import aiohttp

import router
import util.http

class HttpProxyV1(router.ApiHandler):
    async def process(self, args, context):
        (status, headers, body), err = await util.http.async_http('GET', 'http://192.168.1.19:9200')
        if err is not None:
            return None, err
        if status == 200:
            return body.decode('utf-8'), None
        else:
            return None, resp.reason

router.register_api_handler('/api/http/proxy/v1', HttpProxyV1())