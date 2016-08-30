from router.base_handler import register_api
from router.api_handler import ApiHandler

import filter

class HelloWorld(ApiHandler):
    def process(self, args, context):
        return 'Hello world from ApiHandler', None



register_api('hello/v1', HelloWorld([filter.signed_access_filter]))