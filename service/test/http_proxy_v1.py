import router

import util.http

class HttpProxyV1(router.ApiHandler):
    async def process(self, args, context):
        status, reason, headers, raw = await util.http.async_http('GET', 'http://192.168.1.19:9200')
        if status == 200:
            return raw.decode('utf-8'), None
        else:
            return None, reason


router.register_api_handler('/api/http/proxy/v1', HttpProxyV1())