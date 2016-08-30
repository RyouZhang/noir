from router.base_handler import register_api
from router.api_handler import ApiHandler

class HelloWorldV2(ApiHandler):
    def process(self, args, context):
        return 'Hello world V2 from ApiHandler', None


register_api('hello/v2', HelloWorldV2())