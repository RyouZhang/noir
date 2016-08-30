import router
import filter

class HelloWorld(router.ApiHandler):
    def process(self, args, context):
        return 'Hello world from ApiHandler', None


filter.register_api_filter('/api/hello/v1', [filter.signed_filter])
router.register_api_handler('/api/hello/v1', HelloWorld())