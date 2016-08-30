import router

class HelloWorldV2(router.ApiHandler):
    def process(self, args, context):
        return 'Hello world V2 from ApiHandler', None


router.register_api_handler('hello/v2', HelloWorldV2())